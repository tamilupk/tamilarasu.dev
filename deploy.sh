#!/bin/bash
run_instance_op = `aws ec2 run-instances \
                    --image-id ami-0885b1f6bd170450c \
                    --count 1 \
                    --instance-type t2.micro \
                    --key-name m1_mac \
                    --security-group-ids sg-03d06481bfec4701f \
                    --subnet-id subnet-099e8ac0172011cea \
                    --user-data file://user_data.sh`

 awk  'BEGIN { FS = "InstanceId\": \"" } ; { print $2 }' | awk  'BEGIN { FS = "\"" } ; { print $1 }'


aws elbv2 register-targets \
    --target-group-arn arn:aws:elasticloadbalancing:us-east-1:642333780766:targetgroup/tg-def/422948bcc92b9333 \
    --targets Id=i-07f9c890fe06489fb,Port=3000