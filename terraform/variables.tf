variable "test_password" {
  description = "Password for the lab's test users. Set with TF_VAR_test_password; never commit it."
  type        = string
  sensitive   = true
}
