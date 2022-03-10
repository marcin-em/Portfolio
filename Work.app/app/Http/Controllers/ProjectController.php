<?php

namespace App\Http\Controllers;

use App\Models\Project;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ProjectController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return Project::orderBy('start', 'asc')->get();
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'name' => 'required',
            'client' => 'required',
            'start' => 'required',
            'status' => 'required',
            'image' => 'image|mimes:jpeg,png,jpg,gif|nullable|max:2048',
        ]);
        
        $project = new Project;
        $project->name = $request->name;
        $project->client = $request->client;
        $project->start = $request->start;
        $project->status = $request->status;
        $project->info = $request->info;
        $project->cost = $request->cost;

        if($request->hasFile('image'))
        {
            $file = $request->file('image');
            $org_name = $file->getClientOriginalName();
            $filename = time().'_'.$org_name;

            $path = $request->file('image')->storeAs(
                'public/images', $filename
            );
            $project->image = $filename;
        }
        
        $project->save();
        return response()->json([
            'id' => $project->id,
            'name' => $project->name,
            'client' => $project->client,
            'start' => $project->start,
            'status' => $project->status,
            'info' => $project->info,
            'cost' => $project->cost,
            'image' => $project->image,
        ], 200);
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        return Project::find($id);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */


    public function imgDel($id)
    {
        $project = Project::find($id);

        Storage::delete('public/images/'.$project->image);
        $project->image = null;
        $project->save();

        return response()->json([
            'message' => 'Image deleted',
            'image' => $project->image
        ], 200);
    }
    
    public function update(Request $request, $id)
    {
        $request->validate([
            'name' => 'required',
            'client' => 'required',
            'start' => 'required',
            'status' => 'required',
            'image' => 'image|mimes:jpeg,png,jpg,gif|nullable|max:2048',
        ]);
        
        $project = Project::find($id);

        $project->name = $request->input('name');
        $project->client = $request->input('client');
        $project->start = $request->input('start');
        $project->status = $request->input('status');
        $project->info = $request->input('info');
        $project->cost = $request->input('cost');

        if($request->hasFile('image'))
        {
            if(!is_null($project->image))
            {
                Storage::delete('public/images/'.$project->image);
            }
            $file = $request->file('image');
            $org_name = $file->getClientOriginalName();
            $filename = time().'_'.$org_name;

            $path = $request->file('image')->storeAs(
                'public/images', $filename
            );
            $project->image = $filename;
        }
        
        $project->save();

        return response()->json([
            'id' => $project->id,
            'name' => $project->name,
            'client' => $project->client,
            'start' => $project->start,
            'status' => $project->status,
            'info' => $project->info,
            'cost' => $project->cost,
            'image' => $project->image,
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $project = Project::find($id);

        if(!is_null($project->image))
            {
                Storage::delete('public/images/'.$project->image);
                $project->image = null;
            }
        return Project::destroy($id);
    }
}
