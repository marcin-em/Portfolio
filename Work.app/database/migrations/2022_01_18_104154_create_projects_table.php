<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateProjectsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('projects', function (Blueprint $table) {
            $table->id();
            // $table->timestamps();
            $table->string('name', 40);
            $table->string('client');
            $table->string('start');
            $table->integer('cost')->nullable();
            $table->string('info', 200)->nullable();
            $table->enum('status', ['open', 'sent', 'closed'])->default('open');
            $table->string('image')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('projects');
    }
}
