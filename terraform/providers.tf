terraform {
  required_version = ">= 1.6"
  required_providers {
    okta = {
      source  = "okta/okta"
      version = ">= 4.0"
    }
  }
}

# Reads OKTA_ORG_NAME, OKTA_BASE_URL and OKTA_API_TOKEN from the environment,
# so no secret is ever written in code.
provider "okta" {}
