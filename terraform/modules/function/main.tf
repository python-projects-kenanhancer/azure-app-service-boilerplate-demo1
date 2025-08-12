locals {
  function_archive_name = "${var.function_config.name}-${data.archive_file.function_source.output_md5}.zip"
  project_root          = "${path.root}/../"
  source_dir            = "${local.project_root}src"
}

# Generate requirements.txt before creating the archive (generating requirements.txt during terraform apply)
resource "null_resource" "generate_requirements" {
  # Trigger regeneration whenever these files change
  triggers = {
    pyproject_toml = filemd5("${local.project_root}pyproject.toml")
    source_code    = sha1(join("", [for f in fileset(local.source_dir, "**/*.py") : filemd5("${local.source_dir}/${f}")]))
  }

  provisioner "local-exec" {
    command     = "uv pip compile ${local.project_root}pyproject.toml -o ${local.source_dir}/requirements.txt"
    working_dir = local.source_dir
  }
}

# Create the function archive
data "archive_file" "function_source" {
  depends_on  = [null_resource.generate_requirements]
  type        = "zip"
  source_dir  = local.source_dir
  output_path = "${local.project_root}dist/${var.function_config.name}.zip"

  excludes = [
    "**/__pycache__",
    "**/*.pyc",
    "**/*.pyo",
    "**/*.pyd",
    "**/*.rest",
    ".pytest_cache",
    "__pycache__",
    "*.pyc",
    ".Python",
    "env",
    "pip-log.txt",
    "pip-delete-this-directory.txt",
    ".tox",
    ".coverage",
    ".coverage.*",
    ".cache",
    "nosetests.xml",
    "coverage.xml",
    "*,cover",
    "*.log",
    ".pytest_cache"
  ]
}

resource "google_storage_bucket_object" "function_archive" {
  name   = local.function_archive_name
  bucket = var.function_config.source_bucket
  source = data.archive_file.function_source.output_path
}

resource "google_cloudfunctions2_function" "function" {
  name        = "${var.function_config.name}-${var.basic_config.environment}"
  location    = var.basic_config.gcp_region
  description = "Cloud function for ${var.basic_config.environment}"

  build_config {
    runtime     = var.function_config.runtime
    entry_point = var.function_config.entry_point
    source {
      storage_source {
        bucket = var.function_config.source_bucket
        object = google_storage_bucket_object.function_archive.name
      }
    }
  }

  service_config {
    available_memory      = "${var.function_config.available_memory_mb}M"
    timeout_seconds       = var.function_config.timeout_seconds
    environment_variables = var.function_config.environment_variables
    service_account_email = var.function_config.service_account_email
  }
}
