Blender 2.6 LDraw Importer
==========================
Hello everybody! le717 here, reminding you that if you would like to learn more about this project, or donate code to it, you need to read this first.

History Lesson
--------------

This is a [Blender 2.6] (http://www.blender.org) Importer script for the [LDraw System of Tools's Brick Library.] (http://www.ldraw.org) 

> LDraw™ is an open standard for LEGO CAD programs that allow the user to create virtual LEGO models and scenes. You can use it to document models you have
>physically built, create building instructions just like LEGO, render 3D photo realistic images of your virtual models and even make animations. 
>The possibilities are endless. Unlike real LEGO bricks where you are limited by the number of parts and colors, in LDraw nothing is impossible.

There are many LDraw importer scripts for Blender 2.3 available, each one with its own errors and quirks, some that have even been lost over time due to dead 
links. Many people have wanted an updated version of these scripts for a while, but nobody seemed to want to write one.
 
However, David Pluntze did, and posted it [online] (http://projects.blender.org/tracker/index.php?func=detail&aid=30327&group_id=153&atid=467) on Febuary 23, 
2012.
However, the script, written for Blender 2.5, was in poor shape and was imcomplete. By the time I found it in early October 2012, Blender 2.6 was already 
released, and the script would not even activate. I contacted my friend [JrMasterModelBuilder] (http://jrmastermodelbuilder.netai.net) who corrected the 
script for me, and allowed it to be used in Blender 2.6.

From then until January 2013, he and I tried to improve the script as much as possible. Many versions were released, and many bugs were fixed and identified. 
However, since I knew very little Python, the process was a challenge.

After putting off uploading the script to the web for anyone to improve, I finally uploaded here, on GitHub.

Commit Guidelines
-----------------

There are a few guidelines that must be followed at all times when developing the Blender 2.6 LDraw Importer:

* Backward compatibility

* Blender script guidelines

* Separate branches
I've divided the project into three separate, distinct branches: master, unstable, and exporter.

* The **master** branch is where stable, complete, mostly bug-free belongs. It is this code that will make up the next, official release. If one wanted to download the next release and not worry about it being broken, they would download from this branch.
* The **unstable** branch is where all beta, draft, and buggy code belongs. Features that may be harder to implement or take longer to add go here so the master branch does not contain error code.

*All explanations coming soon*