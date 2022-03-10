<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Laravel\Sanctum\HasApiTokens;

class Project extends Model
{
    use HasFactory, HasApiTokens;
    protected $fillable = [
        'name',
        'client',
        'start',
        'cost',
        'info',
        'status',
        'image',
    ];
    public $timestamps = false;
}
