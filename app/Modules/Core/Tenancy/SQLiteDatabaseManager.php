<?php

declare(strict_types=1);

namespace App\Modules\Core\Tenancy;

use Stancl\Tenancy\Contracts\TenantDatabaseManager;
use Stancl\Tenancy\Contracts\TenantWithDatabase;

class SQLiteDatabaseManager implements TenantDatabaseManager
{
    public function createDatabase(TenantWithDatabase $tenant): bool
    {
        try {
            $path = $this->resolveDatabasePath($tenant->database()->getName());
            $directory = dirname($path);

            if (! is_dir($directory)) {
                mkdir($directory, 0755, true);
            }

            return touch($path);
        } catch (\Throwable) {
            return false;
        }
    }

    public function deleteDatabase(TenantWithDatabase $tenant): bool
    {
        try {
            $path = $this->resolveDatabasePath($tenant->database()->getName());

            return ! file_exists($path) || unlink($path);
        } catch (\Throwable) {
            return false;
        }
    }

    public function databaseExists(string $name): bool
    {
        $path = $this->resolveDatabasePath($name);

        return file_exists($path);
    }

    public function makeConnectionConfig(array $baseConfig, string $databaseName): array
    {
        $baseConfig['database'] = $this->resolveDatabasePath($databaseName);
        $baseConfig['foreign_key_constraints'] = env('DB_FOREIGN_KEYS', true);

        return $baseConfig;
    }

    public function setConnection(string $connection): void
    {
        //
    }

    protected function resolveDatabasePath(string $databaseName): string
    {
        $directPath = database_path($databaseName);
        if (file_exists($directPath)) {
            return $directPath;
        }

        $sqlitePath = database_path($databaseName . '.sqlite');
        if (file_exists($sqlitePath)) {
            return $sqlitePath;
        }

        return $directPath;
    }
}
