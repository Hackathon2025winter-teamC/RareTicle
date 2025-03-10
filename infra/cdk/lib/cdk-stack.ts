import { Stack, StackProps } from "aws-cdk-lib";
import { Construct } from "constructs";

import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as elbv2 from "aws-cdk-lib/aws-elasticloadbalancingv2";
import * as targets from "aws-cdk-lib/aws-elasticloadbalancingv2-targets";
import * as rds from "aws-cdk-lib/aws-rds";
import * as iam from "aws-cdk-lib/aws-iam";

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // VPC の作成 (3層構造)
    const vpc = new ec2.Vpc(this, "RareTicleVPC", {
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: "PublicSubnet",
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: "PrivateSubnet",
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
        },
        {
          cidrMask: 24,
          name: "DatabaseSubnet",
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        },
      ],
    });

    // セキュリティグループの作成
    const ec2SecurityGroup = new ec2.SecurityGroup(this, "EC2SecurityGroup", {
      vpc,
      description: "EC2-SG",
      allowAllOutbound: true,
    });

    // IAM ロールの作成（SSM アクセス許可を付与）
    const role = new iam.Role(this, "SSMRole", {
      assumedBy: new iam.ServicePrincipal("ec2.amazonaws.com"),
    });
    // SSM の管理ポリシーをアタッチ
    role.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName("AmazonSSMManagedInstanceCore")
    );

    // `SessionDuration` を 12時間 (43200秒) に設定
    role.addToPolicy(
      new iam.PolicyStatement({
        effect: iam.Effect.ALLOW, // 許可 (Allow) のポリシーを定義
        actions: ["ssm:StartSession"], // AWS Systems Manager (SSM) のセッション開始を許可
        resources: ["*"], // すべてのリソースに適用（特定のEC2インスタンスのARNを指定することも可能）
        conditions: {
          NumericLessThanEquals: { "ssm:SessionDuration": 43200 }, // セッションの最大持続時間を 12時間 (43200秒) に制限
        },
      })
    );

    // EC2 インスタンスの作成 (2台)
    const ec2Instances = [];
    for (let i = 0; i < 2; i++) {
      ec2Instances.push(
        new ec2.Instance(this, `EC2Instance${i + 1}`, {
          vpc,
          vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
          instanceType: ec2.InstanceType.of(
            ec2.InstanceClass.T2,
            ec2.InstanceSize.MICRO
          ),
          machineImage: ec2.MachineImage.latestAmazonLinux2023(),
          securityGroup: ec2SecurityGroup,
          role: role,
        })
      );
      // EC2 にユーザーデータ (Nginx, Django セットアップ)

      // nginx,SSMインストール
      ec2Instances[i].addUserData(
        `#!/bin/bash
      dnf update -y
      dnf install -y amazon-linux-extras nginx git python3 python3-pip
      systemctl start nginx
      systemctl enable nginx
      pip3 install django gunicorn mysqlclient

      # Docker のインストール
      sudo amazon-linux-extras enable docker
      sudo dnf install -y docker
      sudo systemctl enable docker
      sudo systemctl start docker
      sudo usermod -aG docker ec2-user

      # Docker Compose のインストール
      sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
      sudo chmod +x /usr/local/bin/docker-compose
      sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

      # git のインストール
      dnf install -y git

      # SSM エージェントのインストール
      dnf install -y amazon-ssm-agent
      systemctl enable amazon-ssm-agent
      systemctl start amazon-ssm-agent
      echo "Django & Gunicorn installed."
      `
      );
    }

    // ALBのセキュリティグループ　アウトバウンドを設定
    const albSecurityGroup = new ec2.SecurityGroup(this, "ALBSecurityGroup", {
      vpc,
      description: "Allow all outbound traffic",
      allowAllOutbound: true, // すべてのアウトバウンド通信を許可
    });

    // ALB の作成
    const alb = new elbv2.ApplicationLoadBalancer(this, "ALB", {
      vpc,
      internetFacing: true,
    });

    // EC2 インスタンスをターゲットグループに追加
    const targetGroup = new elbv2.ApplicationTargetGroup(this, "TargetGroup", {
      vpc,
      targetType: elbv2.TargetType.INSTANCE,
      targets: [
        new targets.InstanceIdTarget(ec2Instances[0].instanceId),
        new targets.InstanceIdTarget(ec2Instances[1].instanceId),
      ],
      // port: 80,
      port: 8080,
      protocol: elbv2.ApplicationProtocol.HTTP,
      healthCheck: {
        path: "/",
        interval: cdk.Duration.seconds(30),
      },
    });

    // ALB のリスナー設定
    const listener = alb.addListener("Listener", {
      port: 80,
      protocol: elbv2.ApplicationProtocol.HTTP,
      defaultAction: elbv2.ListenerAction.forward([targetGroup]),
    });
    // EC2 のセキュリティグループに ALB からの HTTP 通信を許可:
    ec2SecurityGroup.addIngressRule(
      albSecurityGroup,
      // ec2.Port.tcp(80),
      ec2.Port.tcp(8080),
      "Allow ALB to communicate with EC2"
    );
    // RDS の作成 (プライベートサブネットのみ)
    const rdsSecurityGroup = new ec2.SecurityGroup(this, "RDSSecurityGroup", {
      vpc,
      allowAllOutbound: false,
    });

    const database = new rds.DatabaseInstance(this, "RDSInstance", {
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      engine: rds.DatabaseInstanceEngine.mysql({
        version: rds.MysqlEngineVersion.VER_8_4_3,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T4G,
        ec2.InstanceSize.MICRO
      ),
      // DBのユーザ名を設定、パスワードはSecrets Manager に自動保存
      credentials: rds.Credentials.fromGeneratedSecret("django"),
      multiAz: false,
      allocatedStorage: 20,
      securityGroups: [rdsSecurityGroup],
    });

    // RDS へのセキュリティグループ設定 (EC2 からのみ接続可能)
    rdsSecurityGroup.addIngressRule(
      ec2SecurityGroup,
      ec2.Port.tcp(3306),
      "Allow EC2 to connect to RDS"
    );

    // 出力情報
    new cdk.CfnOutput(this, "ALB DNS Name", { value: alb.loadBalancerDnsName });
  }
}
