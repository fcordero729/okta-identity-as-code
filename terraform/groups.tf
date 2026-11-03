resource "okta_group" "it" {
  name        = "IT"
  description = "IT department, assigned by group rule"
}

resource "okta_group" "finance" {
  name        = "Finance"
  description = "Finance department, assigned by group rule"
}

resource "okta_group" "app_admins" {
  name        = "App-Admins"
  description = "Privileged admins of the demo app; MFA required"
}

# Joiner and mover: membership follows the user's department attribute.
resource "okta_group_rule" "it_by_department" {
  name              = "Department IT"
  status            = "ACTIVE"
  group_assignments = [okta_group.it.id]
  expression_type   = "urn:okta:expression:1.0"
  expression_value  = "user.department==\"IT\""
}

resource "okta_group_rule" "finance_by_department" {
  name              = "Department Finance"
  status            = "ACTIVE"
  group_assignments = [okta_group.finance.id]
  expression_type   = "urn:okta:expression:1.0"
  expression_value  = "user.department==\"Finance\""
}
