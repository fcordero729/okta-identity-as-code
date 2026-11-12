locals {
  users = {
    alex   = { first = "Alex", last = "Rivera", dept = "IT", title = "Systems Engineer" }
    jamie  = { first = "Jamie", last = "Chen", dept = "Finance", status = "DEPROVISIONED" }
    sam    = { first = "Sam", last = "Patel", dept = "Finance" }
    taylor = { first = "Taylor", last = "Brooks", dept = "Finance", status = "SUSPENDED" }
    casey  = { first = "Casey", last = "Nguyen", dept = "IT", status = "SUSPENDED" }
  }
}

resource "okta_user" "lab" {
  for_each   = local.users
  first_name = each.value.first
  last_name  = each.value.last
  login      = "${each.key}@example.com"
  email      = "${each.key}@example.com"
  department = each.value.dept
  title      = lookup(each.value, "title", null)
  status     = lookup(each.value, "status", "ACTIVE")
  password   = var.test_password

  # Refuse to delete any user. Remove this block on purpose to allow a deletion.
  lifecycle {
    prevent_destroy = true
  }
}

# Privileged access is granted explicitly, never by rule.
resource "okta_group_memberships" "app_admins" {
  group_id = okta_group.app_admins.id
  users    = [okta_user.lab["alex"].id]
}