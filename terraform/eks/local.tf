locals {
  cluster_name    = "dig-eks"
  cluster_version = "1.28"

  cluster_endpoint_public_access  = true

  vpc_id                   = "vpc-1234556abcdef"
  subnet_ids               = ["subnet-abcde012", "subnet-bcde012a", "subnet-fghi345a"]
  control_plane_subnet_ids = ["subnet-xyzde987", "subnet-slkjf456", "subnet-qeiru789"]


tags = {
    Environment = "dev"
  }
}