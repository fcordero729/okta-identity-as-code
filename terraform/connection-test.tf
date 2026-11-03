# Reads Okta's built-in Everyone group to prove Terraform can reach your org.
data "okta_group" "everyone" {
  name = "Everyone"
}

output "everyone_group_id" {
  value = data.okta_group.everyone.id
}
