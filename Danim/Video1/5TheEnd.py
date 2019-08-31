from Danim.Contry import *
from Danim.Distribution import LogscaleNumberLine
hair_svg_dir = "Danim\\video1\\file\\T_hair.svg"

#坐标轴设置settings
population_per_circle_area = 1/1.4*1.2 # default: 1.4 billion people is a 1.2unit area circle
xmin = 0
xmax = 10
ymin = 0
ymax = 100
proportion_to_left = 0.9 #default x axis move to 10% empty space left, note its the proportion to the origin
proportion_to_bottom = 0.8
x_scale_factor = (proportion_to_left+1)*FRAME_X_RADIUS/(xmax-xmin)*0.96 # 0.96 is arrow buff
y_scale_factor = (proportion_to_bottom+1)*FRAME_Y_RADIUS/(ymax-ymin)*0.96
NEWORIGIN = [-FRAME_X_RADIUS*proportion_to_left,-FRAME_Y_RADIUS*proportion_to_bottom,0]

mode = "chinese"

#TODO: make it a mobject class

def create_eyes_for_a_circle(
    circle, 
    right_eye_angle = PI/4, 
    height_width_ratio = 1.3, 
    width_radius_ratio = 0.2,
    eye_color = WHITE,
    pupil_color = BLACK,
    pupil_to_eye_ratio = 0.4,
    pupil_black_to_white = 0.2,
    eye_to_origin = 1.5/3.,
    pupil_black_direction = UR,
    pupil_stroke = 4
    ):

    assert(isinstance(circle,Circle))
    assert(right_eye_angle < PI/2)
    origin = circle.get_center()
    radius = get_norm(origin - circle.points[0])
    width = radius* width_radius_ratio
    
    eyes = VGroup()
    
    #create eyes:
    right_eye_unit_vec = np.array([np.cos(right_eye_angle),np.sin(right_eye_angle),0])
    left_eye_unit_vec = np.array([-np.cos(right_eye_angle),np.sin(right_eye_angle),0])

    eyes.left_eye = Circle(radius = width,color = eye_color,num_components = 60)
    eyes.right_eye = Circle(radius = width,color = eye_color,num_components = 60)
    eyes.left_eye.set_fill(eye_color,1)
    eyes.right_eye.set_fill(eye_color,1)

    eyes.left_eye.move_to(origin)
    eyes.right_eye.move_to(origin)

    eyes.left_eye.shift(left_eye_unit_vec*radius*eye_to_origin)
    eyes.right_eye.shift(right_eye_unit_vec*radius*eye_to_origin)
    eyes.left_eye.stretch(height_width_ratio, dim = 1)
    eyes.right_eye.stretch(height_width_ratio, dim = 1)
    
    eyes.add(eyes.right_eye)
    eyes.add(eyes.left_eye)

    #create right pupils:
    eyes.right_pupil = VGroup()

    eyes.right_pupil.pupil_white = Circle(
        radius = width*pupil_to_eye_ratio,
        color = pupil_color,
        stroke_width = pupil_stroke
        ).move_to(
            eyes.right_eye.get_center()
            )
    eyes.right_pupil.pupil_white.set_fill(pupil_color,1)

    #eyes.right_pupil.add(eyes.right_pupil.pupil_white)

    eyes.right_pupil.pupil_black = Circle(
        radius = width*pupil_to_eye_ratio*pupil_black_to_white,
        color = eye_color,
        num_components = 60,
        stroke_width = pupil_stroke
        ).move_to(eyes.right_pupil.pupil_white.get_center())


    eyes.right_pupil.pupil_black.shift(
        eyes.right_pupil.pupil_white.get_boundary_point(pupil_black_direction) - 
        eyes.right_pupil.pupil_black.get_boundary_point(pupil_black_direction))
    eyes.right_pupil.pupil_black.set_fill(eye_color,1)
    #eyes.right_pupil.add(eyes.right_pupil.pupil_black)

    #create left pupil:
    eyes.left_pupil = VGroup()

    eyes.left_pupil.pupil_white = Circle(
        radius = width*pupil_to_eye_ratio,
        color = pupil_color,
        stroke_width = pupil_stroke
        ).move_to(
            eyes.left_eye.get_center()
            )
    eyes.left_pupil.pupil_white.set_fill(pupil_color,1)
    #eyes.left_pupil.add(eyes.left_pupil.pupil_white)

    eyes.left_pupil.pupil_black = Circle(
        radius = width*pupil_to_eye_ratio*pupil_black_to_white,
        color = eye_color,
        num_components = 60,
        stroke_width = pupil_stroke
        ).move_to(eyes.left_pupil.pupil_white.get_center())
    eyes.left_pupil.pupil_black.shift(
        eyes.left_pupil.pupil_white.get_boundary_point(pupil_black_direction) - 
        eyes.left_pupil.pupil_black.get_boundary_point(pupil_black_direction))
    eyes.left_pupil.pupil_black.set_fill(eye_color,1)
    #eyes.left_pupil.add(eyes.left_pupil.pupil_black)

    #add sequence matter
    eyes.add(
        eyes.right_pupil.pupil_white,
        eyes.left_pupil.pupil_white,
        eyes.right_pupil.pupil_black,
        eyes.left_pupil.pupil_black
        )


    return eyes

def eyes_blink_animation(eyes,**kwargs):
    assert(isinstance(eyes,VGroup)&hasattr(eyes,"right_eye"))
    eye_bottom_y = eyes.left_eye.get_bottom()[1]
    return ApplyMethod(
        eyes.apply_function,
        lambda p: [p[0], eye_bottom_y, p[2]],
        rate_func = squish_rate_func(there_and_back),
        **kwargs
        )

def eyes_look_at(eyes,thing_to_look,return_animation):

    #TODO:things_to_look can be a mobject or a coordinate
    #now thing_to_look is just a mobject 
    assert(isinstance(eyes,VGroup)&hasattr(eyes,"right_eye"))
    assert(isinstance(thing_to_look,Mobject))
    
    #calculate the shift vector
    mcenter = thing_to_look.get_center()
    rcenter = eyes.right_eye.get_center()
    lcenter = eyes.left_eye.get_center()

    rstart = eyes.right_pupil.pupil_white.get_boundary_point(mcenter - rcenter)
    rend = eyes.right_eye.get_boundary_point(mcenter - rcenter)
    lstart = eyes.left_pupil.pupil_white.get_boundary_point(mcenter - lcenter)
    lend = eyes.left_eye.get_boundary_point(mcenter - lcenter)
    
    right_eye_shift_vec = - rstart + rend
    left_eye_shift_vec = - lstart + lend



    if return_animation:
        return AnimationGroup(
            ApplyMethod(
                VGroup(
                    eyes.left_pupil.pupil_white,
                    eyes.left_pupil.pupil_black
                    ).shift,
                left_eye_shift_vec
                ),
            ApplyMethod(
                VGroup(
                    eyes.right_pupil.pupil_white,
                    eyes.right_pupil.pupil_black
                    ).shift,
                right_eye_shift_vec
                )
            )
    else:
        return right_eye_shift_vec, left_eye_shift_vec

def eyes_back_to_center(eyes):
    rcenter = eyes.right_eye.get_center()
    lcenter = eyes.left_eye.get_center()

    VGroup(eyes.left_pupil.pupil_white,eyes.left_pupil.pupil_black).shift(lcenter)


class TheEnd(Scene):

    def construct(self, mode = mode):
        #logotag
        logotag = TextMobject("引力子G @B站").scale(0.4)
        logotag.to_edge(DR)
        logotag.shift(0.4*DOWN+0.4*RIGHT)
        logotag.asdfi = 1# no use, for not fadeout in the end
        self.add(logotag)

        #--------------------------------创建坐标系
        y_axis = NumberLine(
            x_min = ymin,
            x_max = ymax,
            label_direction = LEFT,
            include_tip = True,
            tick_frequency= 10,
            ).rotate(90 * DEGREES, about_point=ORIGIN)
        x_axis = LogscaleNumberLine(x_max = xmax, log_factor = 250,log_base = 2,include_tip = True)
        
        x_axis.move_to(ORIGIN,aligned_edge=LEFT)
        y_axis.move_to(ORIGIN,aligned_edge=DOWN)

        x_axis.stretch_about_point(x_scale_factor, 0, ORIGIN)
        y_axis.stretch_about_point(y_scale_factor, 1, ORIGIN)
        
        axes = VGroup()
        axes.x_axis = x_axis
        axes.y_axis = y_axis
        axes.add(x_axis)
        axes.add(y_axis)

        axes.shift(NEWORIGIN)

        axes.x_axis.add_numbers(*[1,2,3,4,5,6,7,8,9])
        axes.new_num = VGroup()
        for index in [5,6,7,8]:
            location = axes.x_axis.numbers[index].get_center()
            axes.x_axis.numbers[index].move_to([-15,-15,0])
            num = TextMobject(str(int(axes.x_axis.numbers[index].get_value()/1000))+"k").scale(0.7)
            num.move_to(location + 0.05*UP)
            axes.new_num.add(num)

        axes.add(axes.new_num)

        axes.y_axis.add_numbers(*np.arange(10,100,10))  


        y_axis_label_text = TextMobject("人均寿命").scale(0.6)
        y_axis_label_text.next_to(axes.y_axis.number_to_point(95), RIGHT+UP)

        x_axis_label_text = TextMobject("人均GDP").scale(0.6)
        x_axis_label_text.next_to(axes.x_axis.number_to_point(9.5), UP)

        #create year lable:
        year_lable = Integer(2018,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)

        #CREATE THE CIRCLES AND AREA RECT
        area_rect = []
        area_rect_lable = []
        areas = []
        rect = VGroup()
        bubbles = VGroup()
        for i,area in enumerate(THE_WHOLE_WORLD):

            areas.append(Area(area,show_CN_name = False))
            area_rect.append(Rectangle(height = 0.2, width = 0.5,color = AREA_COLOR_MAP[i],fill_opacity = 1))
            
            if i == 0:
                area_rect[i].next_to(year_lable,6*DOWN)

            else:
                area_rect[i].next_to(area_rect[i-1],DOWN)
            area_rect_lable.append(TextMobject(CH_THE_WHOLE_WORLD[i]).scale(0.4))
            area_rect_lable[i].next_to(area_rect[i],LEFT)

            rect.add(area_rect[i],area_rect_lable[i])

            #notice: before run this function 
            #change get_both_fertandlife_point() 
            #function in Contry.py to Version 2
            areas[i].generate_all_contry_circles(
                years_date=2018,
                COLORMAT = [AREA_COLOR_MAP[i]],
                if_switch_on =False,
                Axes = axes
                )

            for contry in areas[i].contry_list:
                if contry.name == "China":
                    china = contry
                elif contry.name == "United States":
                    usa = contry


                bubbles.add(contry.shape)


        lable_CN = TextMobject("中国", color = RED).scale(0.8)
        lable_CN.next_to(china.shape,UP)

        self.add(VGroup(axes,y_axis_label_text,x_axis_label_text,year_lable,bubbles,rect,lable_CN))
        self.wait()


        #stage 1:Highlight china

        #CHECK whether circle 2 is inside of china circle
        origin1 = china.shape.get_center()
        point1 = china.shape.points[0]
        radius1 = get_norm(point1 - origin1)

        def is_inside_china(circle2,origin1 = origin1,radius1 = radius1):
            assert(isinstance(circle2,Circle))
            origin2 = circle2.get_center()
            dis = get_norm(origin2 - origin1)
            if dis>radius1:
                return False
            else:
                return True

        circles_to_fadeout = VGroup()
        circles_to_dim_animation = []
        for area in areas:
            for i,contry in enumerate(area.contry_list):
                if (not contry.name == "China") and (is_inside_china(circle2 = contry.shape)):
                    circles_to_fadeout.add(contry.shape)
                elif (not contry.name == "China") and (not is_inside_china(circle2 = contry.shape)):
                    circles_to_dim_animation.append(ApplyMethod(contry.shape.fade,0.8))

        china.shape.eyes = create_eyes_for_a_circle(china.shape)
        self.play(
            AnimationGroup(
                ApplyMethod(
                    china.shape.set_fill,
                    RED,
                    1
                    ),
                FadeOut(circles_to_fadeout),
                FadeIn(china.shape.eyes),
                *circles_to_dim_animation,
                run_time = 2
                )
            )


        self.wait()
        
        self.play(eyes_blink_animation(china.shape.eyes,run_time = 0.6))
        self.play(eyes_blink_animation(china.shape.eyes,run_time = 0.6))
        self.play(eyes_blink_animation(china.shape.eyes,run_time = 0.6))
        self.wait()
        #stage 2: show Shanghai


        def high_light_a_part(
            pop, 
            life_expect,
            gdp_per_cap,
            contry, 
            direction, 
            part_name,
            convert_from_local_currency_to_PPP_dollar,
            contry_eyes = None,
            stroke_width = 1,
            color = RED,
            num_components = 60,
            lable_next_to_direction = DOWN,
            creation_time = 3,
            transfer_time = 3
            ):

            part_radius = math.sqrt(pop/1000000000*population_per_circle_area/np.pi)
            origin_x_GDPperCap = math.log(np.divide(gdp_per_cap/convert_from_local_currency_to_PPP_dollar,250),2)#log_factor = 250,log_base = 2
            part_center = np.array(coordinate_origin_to_new(np.array([origin_x_GDPperCap,life_expect,0])))

            part = Circle(radius = part_radius,color = BLACK,stroke_width = stroke_width,num_components =num_components)
            part.set_fill(color,1)

            shift_vec = contry.shape.get_boundary_point(direction) - part.get_boundary_point(direction)
            part.shift(shift_vec)

            part_backgroud = Circle(radius = part_radius,color = BLACK)
            part_backgroud.set_fill(BLACK,1)
            part_backgroud.shift(shift_vec)

            part_lable = TextMobject(part_name, color = color).scale(0.3)
            part_lable.next_to(part,lable_next_to_direction)

            animations = []
            animations.append(Write(part_lable))
            animations.append(FadeIn(part_backgroud))
            animations.append(FadeIn(part))
            if contry_eyes is not None:
                animations.append(eyes_look_at(contry_eyes,part,True))

            self.play(
                *animations,
                run_time = creation_time
                )

            self.wait()

            animations = []
            animations.append(ApplyMethod(VGroup(part,part_lable).shift,part_center-part.get_center()))

            if contry_eyes is not None:
                dot = Dot().move_to(part_center)
                dot.set_opacity(0)
                animations.append(eyes_look_at(contry_eyes,dot,True))

            self.play(
                *animations,
                run_time = transfer_time
                )


        #HIGHTLIGHT shanghai
        high_light_a_part(
            24200000, 
            83.63,
            135000,
            china, 
            DOWN+RIGHT, 
            "上海",
            4,
            contry_eyes = china.shape.eyes,
            stroke_width = 0.5,
            color = RED,
            num_components = 60,
            lable_next_to_direction = 0.2*DOWN+0.5*RIGHT,
            creation_time = 3,
            transfer_time = 3
            )
        self.wait()

        self.play(
            eyes_blink_animation(china.shape.eyes),
            )
        self.play(
            eyes_blink_animation(china.shape.eyes),
            )
        USD_converate_ratio = 59531.66/54898# from US dollar to PPP dollar fixed in 2011
        #HIGHTLIGHT 澳门
        high_light_a_part(
            630000, 
            89.68,
            8.64*10000,
            china, 
            DOWN+LEFT, 
            "澳门",
            USD_converate_ratio,
            contry_eyes = china.shape.eyes,
            stroke_width = 0.5,
            color = RED,
            num_components = 60,
            lable_next_to_direction = 0.1*DOWN+0.1*LEFT,
            creation_time = 3,
            transfer_time = 3
            )

        # hight light usa:---------------------------------------------------
        origin1 = usa.shape.get_center()
        point1 = usa.shape.points[0]
        radius1 = get_norm(point1 - origin1)

        def is_inside_usa(circle2,origin1 = origin1,radius1 = radius1):
            assert(isinstance(circle2,Circle))
            origin2 = circle2.get_center()
            dis = get_norm(origin2 - origin1)
            if dis>radius1:
                return False
            else:
                return True

        #------------------

        circles_to_fadeout = VGroup()

        for area in areas:
            for i,contry in enumerate(area.contry_list):
                if (not contry.name == "United States") and (is_inside_usa(circle2 = contry.shape)):
                    circles_to_fadeout.add(contry.shape)
                
        usa.shape.eyes = create_eyes_for_a_circle(
            usa.shape,
            eye_to_origin = 1/3,
            right_eye_angle = PI/8,
            height_width_ratio=1.5,
            pupil_to_eye_ratio = 0.4,
            pupil_black_to_white = 0.15,
            pupil_stroke = 1,
            width_radius_ratio = 0.2)

        # I'm sorry, I just can't resist...
        # it's not meant to be offensive, 
        # just trying to make more fun.
        '''
        T_hair = SVGMobject(hair_svg_dir,color = ORANGE,stroke_width = 2).scale(0.25)
        T_hair.set_fill(YELLOW,1)
        T_hair.next_to(usa.shape,UP)
        T_hair.shift(0.7*DOWN+0.1*RIGHT)
        '''
        usa_lable = TextMobject("美国",color = BLUE).scale(0.8)
        usa_lable.next_to(usa.shape,DOWN)

        self.play(
            AnimationGroup(
                ApplyMethod(
                    usa.shape.set_fill,
                    BLUE,
                    1
                    ),
                FadeOut(circles_to_fadeout),
                FadeIn(usa.shape.eyes),
                #ShowCreation(T_hair),
                Write(usa_lable),
                run_time = 2
                )
            )

        self.wait()
        
        self.play(
            AnimationGroup(
                eyes_blink_animation(china.shape.eyes),
                eyes_blink_animation(usa.shape.eyes)
                )
            )
        self.play(
            AnimationGroup(
                eyes_look_at(usa.shape.eyes,china.shape,True),
                eyes_look_at(china.shape.eyes,usa.shape,True)
                )
            )
        self.play(
            AnimationGroup(
                eyes_blink_animation(china.shape.eyes),
                eyes_blink_animation(usa.shape.eyes)
                )
            )
        self.play(
            AnimationGroup(
                eyes_blink_animation(china.shape.eyes),
                eyes_blink_animation(usa.shape.eyes)
                )
            )

        self.play()

        # hight light DC, Massachusetts, Idaho,Mississippi :---------------------------------------------------
        # data source :https://en.wikipedia.org/wiki/List_of_U.S._states_by_GDP_per_capita
        # data source :https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_life_expectancy
        

        # DC:
        high_light_a_part(
            200277,  #in 2017
            77.1,# in 2017
            82989,
            usa, 
            RIGHT+2*DOWN, 
            "华盛顿DC",
            USD_converate_ratio,
            contry_eyes = usa.shape.eyes,
            stroke_width = 0.5,
            color = BLUE,
            num_components = 60,
            lable_next_to_direction = 0.3*DOWN,
            creation_time = 1,
            transfer_time = 1
            )

        self.wait(0.5)

        # Massachusetts:
        high_light_a_part(
            6.902*100*10000, 
            80.66,# in 2016
            82480,# in 2017
            usa, 
            DOWN, 
            "马萨诸塞州",
            USD_converate_ratio,
            contry_eyes = usa.shape.eyes,
            stroke_width = 0.5,
            color = BLUE,
            num_components = 60,
            lable_next_to_direction = 0.1*DOWN,
            creation_time = 1,
            transfer_time = 1
            )

        self.wait(0.5)

        #Idaho
        high_light_a_part(
            1.754*100*10000, 
            79,# in 2017
            43430,# in 2018
            usa, 
            LEFT+DOWN, 
            "爱达荷州",
            USD_converate_ratio,
            contry_eyes = usa.shape.eyes,
            stroke_width = 0.5,
            color = BLUE,
            num_components = 60,
            lable_next_to_direction = 0.1*DOWN+0.2*LEFT,
            creation_time = 1,
            transfer_time = 1
            )

        self.wait()
        #Mississippi
        high_light_a_part(
            2.987*100*10000, 
            74.5,# in 2017
            37948,# in 2018
            usa, 
            LEFT, 
            "密西西比",
            USD_converate_ratio,
            contry_eyes = usa.shape.eyes,
            stroke_width = 0.5,
            color = BLUE,
            num_components = 60,
            lable_next_to_direction = 0.1*LEFT,
            creation_time = 1,
            transfer_time = 1
            )

        self.wait(0.5)



        # FADEOUT EVERYTHING
        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)
        self.wait(1)
        
        #introduction to damin:

        Intro1 = TextMobject("想制作自己的数据可视化视频吗?",color = BLUE).scale(0.8)
        Intro2 = TextMobject("访问: github.com/graviton1221/Danim",tex_to_color_map={"访问:": BLUE}).scale(0.8)
        Intro2.next_to(Intro1,DOWN)
        self.play(Write(Intro1),run_time = 3)
        self.wait()
        self.play(Write(Intro2),run_time = 3)
        self.wait(3)

        self.play(FadeOut(VGroup(Intro1,Intro2)),run_time = 2)
        self.wait()


        Intro1 = TextMobject("视频中数据均源于 Gapminder",color = YELLOW).scale(0.8)
        Intro1.shift(3*UP)
        Intro2 = TextMobject("访问：gapminder.org",tex_to_color_map={"访问：": YELLOW}).scale(0.8)
        Intro2.next_to(Intro1,DOWN)

        Intro3 = TextMobject("制作:引力子G",tex_to_color_map={"引力子G": RED}).scale(0.8)
        Intro3.next_to(Intro2,DOWN)
        Intro4 = TextMobject("配音:爱唱歌的小火锅",tex_to_color_map={"爱唱歌的小火锅": GOLD}).scale(0.8)
        Intro4.next_to(Intro3,DOWN)
        Intro5 = TextMobject("因水平有限",color = GREEN).scale(0.8)
        Intro5.next_to(Intro4,DOWN)
        Intro6 = TextMobject("视频中若出现错误",color = GREEN).scale(0.8)
        Intro6.next_to(Intro5,DOWN)
        Intro7 = TextMobject("烦请指正",color = GREEN).scale(0.8)
        Intro7.next_to(Intro6,DOWN)

        self.play(Write(Intro1),run_time = 3)
        self.wait()
        self.play(Write(Intro2),run_time = 3)
        self.wait(3)
        '''
        self.play(FadeOut(VGroup(Intro1,Intro2)),run_time = 2)
        self.wait()
        '''
        self.play(Write(Intro3),run_time = 3)
        self.wait()
        self.play(Write(Intro4),run_time = 3)
        self.wait()
        self.play(Write(VGroup(Intro5,Intro6,Intro7)),run_time = 3)
        self.wait(3)

        self.play(FadeOut(VGroup(Intro1,Intro2,Intro3,Intro4,Intro5,Intro6,Intro7)),run_time = 2)
        self.wait()

        
