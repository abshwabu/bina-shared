<?php

declare(strict_types=1);

use Illuminate\Support\Facades\Route;
use App\Modules\HR\Controllers\EmployeeController;
use App\Modules\HR\Controllers\AttendanceController;
use App\Modules\HR\Controllers\LeaveController;
use App\Modules\HR\Controllers\DepartmentController;
use App\Modules\HR\Controllers\PositionController;
use App\Modules\HR\Controllers\EmployeeDocumentController;
use App\Modules\HR\Controllers\RecruitmentController;

// ── Public Careers / Job Application Form Routes ──────────────────────────────
Route::prefix('api/public/careers')->group(function () {
    Route::get('jobs/{idOrSlug}', [RecruitmentController::class, 'publicShow']);
    Route::post('jobs/{idOrSlug}/apply', [RecruitmentController::class, 'publicSubmit']);
});

// ── Authenticated HR Routes ──────────────────────────────────────────────────
Route::prefix('api/hr')->middleware(['auth:api,sanctum', 'reject-mfa-token'])->group(function () {
    // Employees
    Route::get('employees', [EmployeeController::class, 'index'])->middleware('permission:hr.employees.view');
    Route::post('employees', [EmployeeController::class, 'store'])->middleware('permission:hr.employees.create');
    Route::get('employees/{id}', [EmployeeController::class, 'show'])->middleware('permission:hr.employees.view');
    Route::patch('employees/{id}', [EmployeeController::class, 'update'])->middleware('permission:hr.employees.edit');
    Route::delete('employees/{id}', [EmployeeController::class, 'destroy'])->middleware('permission:hr.employees.edit');
    Route::get('employees/{id}/leave-balances', [EmployeeController::class, 'leaveBalances'])->middleware('permission:hr.leave.view');
    Route::get('employees/{id}/attendance', [EmployeeController::class, 'attendance'])->middleware('permission:hr.attendance.view');
    Route::post('employees/{id}/reset-password', [EmployeeController::class, 'resetPassword'])->middleware('permission:hr.employees.edit');

    // Employee Documents
    Route::get('employees/{id}/documents', [EmployeeDocumentController::class, 'index'])->middleware('permission:hr.employees.view');
    Route::post('employees/{id}/documents', [EmployeeDocumentController::class, 'store'])->middleware('permission:hr.employees.edit');
    Route::get('employees/{id}/documents/{documentId}', [EmployeeDocumentController::class, 'show'])->middleware('permission:hr.employees.view');
    Route::get('employees/{id}/documents/{documentId}/download', [EmployeeDocumentController::class, 'download'])->middleware('permission:hr.employees.view');
    Route::delete('employees/{id}/documents/{documentId}', [EmployeeDocumentController::class, 'destroy'])->middleware('permission:hr.employees.edit');

    // Departments
    Route::get('departments', [DepartmentController::class, 'index'])->middleware('permission:hr.employees.view');
    Route::post('departments', [DepartmentController::class, 'store'])->middleware('permission:hr.employees.edit');
    Route::get('departments/{id}', [DepartmentController::class, 'show'])->middleware('permission:hr.employees.view');
    Route::patch('departments/{id}', [DepartmentController::class, 'update'])->middleware('permission:hr.employees.edit');
    Route::delete('departments/{id}', [DepartmentController::class, 'destroy'])->middleware('permission:hr.employees.edit');

    // Positions
    Route::get('positions', [PositionController::class, 'index'])->middleware('permission:hr.employees.view');
    Route::post('positions', [PositionController::class, 'store'])->middleware('permission:hr.employees.edit');
    Route::get('positions/{id}', [PositionController::class, 'show'])->middleware('permission:hr.employees.view');
    Route::patch('positions/{id}', [PositionController::class, 'update'])->middleware('permission:hr.employees.edit');
    Route::delete('positions/{id}', [PositionController::class, 'destroy'])->middleware('permission:hr.employees.edit');

    // Attendance
    Route::get('attendance/my-status', [AttendanceController::class, 'myStatus']);
    Route::post('attendance/clock-in', [AttendanceController::class, 'clockIn']);
    Route::post('attendance/clock-out', [AttendanceController::class, 'clockOut']);
    Route::get('attendance', [AttendanceController::class, 'index'])->middleware('permission:hr.attendance.view');
    Route::get('attendance/summary', [AttendanceController::class, 'summary'])->middleware('permission:hr.attendance.view');

    // Leave
    Route::get('leave/types', [LeaveController::class, 'types']);
    Route::get('leave/requests', [LeaveController::class, 'index'])->middleware('permission:hr.leave.view');
    Route::post('leave/requests', [LeaveController::class, 'store']);
    Route::patch('leave/requests/{id}/approve', [LeaveController::class, 'approve'])->middleware('permission:hr.leave.approve');
    Route::patch('leave/requests/{id}/reject', [LeaveController::class, 'reject'])->middleware('permission:hr.leave.approve');
    Route::patch('leave/requests/{id}/cancel', [LeaveController::class, 'cancel']);

    // Job Opportunities & Recruitment
    Route::get('jobs/stats', [RecruitmentController::class, 'stats'])->middleware('permission:hr.employees.view');
    Route::get('jobs', [RecruitmentController::class, 'index'])->middleware('permission:hr.employees.view');
    Route::post('jobs', [RecruitmentController::class, 'store'])->middleware('permission:hr.employees.edit');
    Route::get('jobs/{id}', [RecruitmentController::class, 'show'])->middleware('permission:hr.employees.view');
    Route::patch('jobs/{id}', [RecruitmentController::class, 'update'])->middleware('permission:hr.employees.edit');
    Route::delete('jobs/{id}', [RecruitmentController::class, 'destroy'])->middleware('permission:hr.employees.edit');

    // Job Applications
    Route::get('jobs/{id}/applications', [RecruitmentController::class, 'applications'])->middleware('permission:hr.employees.view');
    Route::get('jobs/{id}/applications/{applicationId}/files/{fileType}', [RecruitmentController::class, 'downloadApplicationFile'])->middleware('permission:hr.employees.view');
    Route::patch('jobs/{id}/applications/{applicationId}', [RecruitmentController::class, 'updateApplication'])->middleware('permission:hr.employees.edit');
    Route::delete('jobs/{id}/applications/{applicationId}', [RecruitmentController::class, 'deleteApplication'])->middleware('permission:hr.employees.edit');
});
