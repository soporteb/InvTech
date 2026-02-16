$ErrorActionPreference = "Stop"

if (!(Get-Command psql -ErrorAction SilentlyContinue)) {
  throw "psql is required but was not found. Install PostgreSQL client tools first."
}

if (Test-Path ".env") {
  Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*#") { return }
    if ($_ -match "^\s*$") { return }
    $parts = $_.Split('=',2)
    if ($parts.Count -eq 2) {
      [Environment]::SetEnvironmentVariable($parts[0], $parts[1])
    }
  }
}

$db = if ($env:POSTGRES_DB) { $env:POSTGRES_DB } else { "invtech" }
$user = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "invtech" }
$pass = if ($env:POSTGRES_PASSWORD) { $env:POSTGRES_PASSWORD } else { "invtech" }
$admin = if ($env:PGADMIN_USER) { $env:PGADMIN_USER } else { "postgres" }

if ($env:PGADMIN_PASSWORD) {
  $env:PGPASSWORD = $env:PGADMIN_PASSWORD
}

psql -U $admin -d postgres -c @"
DO `$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$user') THEN
      CREATE ROLE $user LOGIN PASSWORD '$pass';
   ELSE
      ALTER ROLE $user WITH LOGIN PASSWORD '$pass';
   END IF;
END
`$$;
"@

$exists = psql -U $admin -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db'"
if ($exists.Trim() -ne "1") {
  psql -U $admin -d postgres -c "CREATE DATABASE $db OWNER $user;"
}

psql -U $admin -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $db TO $user;"
Write-Host "Local PostgreSQL role/database ensured: user=$user db=$db"
