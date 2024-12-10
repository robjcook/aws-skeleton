When using Terraform to create an AWS IAM role, it's common to configure the role's trust policy (assume role policy) to reference the same role. This can create a circular dependency issue because the role can't fully exist until its assume role policy is defined. Here's how to handle it without lifecycle issues:

### Solution: Use Terraform's `aws_iam_policy_document` for Dynamic Policies
You can create the assume role policy using the `aws_iam_policy_document` resource and explicitly refer to the role's ARN after it has been created.

Here’s an example:

```hcl
# Create the role
resource "aws_iam_role" "example" {
  name               = "example-role"
  assume_role_policy = data.aws_iam_policy_document.example.json
}

# Create the assume role policy document
data "aws_iam_policy_document" "example" {
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.example.arn] # Reference the role itself
    }

    actions = ["sts:AssumeRole"]
  }
}
```

### Why This Works
1. **Separate Data Block:** The `aws_iam_policy_document` is a data source, meaning it is computed dynamically by Terraform. It calculates the JSON for the trust policy only after the role's ARN is available.
   
2. **No Lifecycle Issues:** By separating the trust policy from the `aws_iam_role` resource, Terraform avoids a circular dependency because the `assume_role_policy` is provided as precomputed JSON, not as a direct reference to another resource.

### Additional Notes
- Ensure the role's ARN is stable (e.g., don’t use random strings in the role name) to minimize drift.
- If you need to update the trust relationship later, you can modify the `aws_iam_policy_document` without recreating the role.
