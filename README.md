# Danim

Animation Tools for Data visualization, based on Manim of 3blue1brown

This is Data Animation Tool that creates gif or mp4 video of animated data.

A tool that let your data talk!

Here are some achieved features of this tools: (will add more in the future)


### 1.Bubble chart animation:

Animate the bubble chart, the effects is as follows：
this gif may load for a while...
<img src="image/DEMO1.gif" width="500px" height="281px">

*DATA source: gapminder & UN

### 2.Distribution chart animation:
You can have multiple choices:
Show the distribution
See how it changes through time
Stack different distributions together

the effects is as follows： 
again... please be patient, this gif may load for a while...
<img src="image/DEMO2.gif" width="500px" height="281px">

*DATA source: gapminder & UN

### 3.A lot more to come.... 
There are many ideas that I'm currently developing, 

3b1b/manim is really a very powerful tool.

Feel free to contact me if you have any good ideas, welcome to contribute!


# Installation

Danim is based on Python and manim,

so you need to install python3.7 and 3b1b/manim

The installation guide for 3b1b/manim is at (https://github.com/3b1b/manim)

Once you have done manim installation, download the danim and release it in the origin manim folder.

Go to the manim folder and run the following code

```sh
python -m manim Danim/BubbleChart/BubbleChartAnimation.py BubbleChartAnimation -p
```

you will have your first Bubble Chart Video created.


### Customize your own bubble chart animation:

You can change the data in DATA/X.csv and DATA/Y.csv and DATA/R.csv 

You can change the axes settings in BubbleChart/bubble_constants.py
