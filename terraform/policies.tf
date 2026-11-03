resource "okta_app_signon_policy" "demo" {
  name        = "Demo App Policy"
  description = "MFA for admins, password for everyone else"
}

resource "okta_app_signon_policy_rule" "admins_mfa" {
  policy_id                   = okta_app_signon_policy.demo.id
  name                        = "App-Admins require MFA"
  priority                    = 1
  access                      = "ALLOW"
  groups_included             = [okta_group.app_admins.id]
  factor_mode                 = "2FA"
  re_authentication_frequency = "PT2H"
}
