from Danim.Contry import *
'''
Contry_Group = [
    "Afghanistan","Australia",
    "Canada","Chile","Cuba"
    ,"Egypt","France","Germany","Greece","India","Indonesia",
    "Iran","Italy","Japan","Libya","New Zealand","North Korea","Pakistan","Russia","Saudi Arabia","South Korea",
    "Spain","Sweden","Switzerland","Turkey","Uganda","United Kingdom","Vietnam","Zambia"
    ]
'''


#坐标轴设置axes settings
population_per_circle_area = 1/1.4*1.2 # default: 1.4 billion people is a 1.2unit area circle
xmin = 0
xmax = 100
ymin = 0
ymax = 10
proportion_to_left = 0.9 #default x axis move to 10% empty space left, note its the proportion to the origin
proportion_to_bottom = 0.8
x_scale_factor = (proportion_to_left+1)*FRAME_X_RADIUS/(xmax-xmin)*0.96 # 0.96 is arrow buff
y_scale_factor = (proportion_to_bottom+1)*FRAME_Y_RADIUS/(ymax-ymin)*0.96
NEWORIGIN = [-FRAME_X_RADIUS*proportion_to_left,-FRAME_Y_RADIUS*proportion_to_bottom,0]

#文件位置:
CN_pic_dir = "Danim\\video1\\file\\china.svg"
CN_south_china_sea_dir = "Danim\\video1\\file\\china_map_BU.svg"
USA_pic_dir = "Danim\\video1\\file\\usa.svg"

mode = "chinese"

class BubbleChartExpain(Scene):

    def construct(self, mode = mode):
        #logotag
        logotag = TextMobject("引力子G @B站").scale(0.4)
        logotag.to_edge(DR)
        logotag.shift(0.4*DOWN+0.4*RIGHT)
        logotag.asdfi = 1# no use, for not fadeout in the end
        self.add(logotag)
        self.wait(1)
        
        #introducing china:
        chinamap = VGroup() 
        chinamap.add(SVGMobject(file_name = CN_pic_dir,fill_opacity = 0.7, fill_color = RED,unpack_groups = True ).scale(2.5))
        CN_south_china_sea = VGroup()
        CN_south_china_sea.add(SVGMobject(file_name = CN_south_china_sea_dir,fill_opacity = 0.7, fill_color = RED ).scale(2.5))
        height = CN_south_china_sea.get_height() + 0.1
        width = CN_south_china_sea.get_width() + 0.1
        SCS_rect = Rectangle(height= height,width = width,color = RED) #CN_south_china_sea.next_to(chinamap,RIGHT+DOWN)
        CN_south_china_sea.add(SCS_rect)
        CN_south_china_sea.scale(0.2)
        CN_south_china_sea.next_to(chinamap,LEFT+DOWN)
        CN_south_china_sea.shift(1*UP+2.5*RIGHT)
        CN_south_china_sea.stretch(0.8,dim = 0)
        chinamap.add(CN_south_china_sea)
        
        #chinamap.shift(0.5*DOWN)

        #show china map
        if mode == "chinese":
            CN_name = TextMobject("中国",color = RED)
        else:
            CN_name = TextMobject("China",color = RED)

        CN_name.shift(3.5*DOWN+0.3*RIGHT)
        year_lable = Integer(2018,group_with_commas = False,color = TEAL).scale(1)
        year_lable.to_edge(UR)
        year_lable.shift(0.4*UP+0.1*RIGHT)

        self.play(
            AnimationGroup(
                FadeIn(chinamap),
                FadeIn(year_lable),
                Write(CN_name)),
                run_time = 2
                )
        
        self.wait(2)
        
        #introduce population
        if mode == "chinese":
            intro1 = TextMobject("总人口数:").scale(0.7)
            intro2 = DecimalNumber(13.9,color = RED).scale(0.7)
            intro3 = TextMobject("亿").scale(0.7)

        else:
            intro1 = TextMobject("Population:").scale(0.7)
            intro2 = DecimalNumber(1.3,color = RED).scale(0.7)
            intro3 = TextMobject("billion").scale(0.7)

        intro1.shift(3.4*UP + 0.7*LEFT)
        intro2.next_to(intro1,RIGHT)
        intro3.next_to(intro2,RIGHT)
        pop_intro = VGroup(intro1,intro2,intro3)

        self.play(Write(pop_intro),run_time=2)
        self.wait()

        #introduce fertality rate
        if mode == "chinese":
            intro4 = TextMobject("每户孩子数:").scale(0.7)
            intro5 = DecimalNumber(1.6,color = RED,num_decimal_places=1).scale(0.7)
            intro6 = TextMobject("个").scale(0.7)

        else:
            intro4 = TextMobject("Children per family:").scale(0.7)
            intro5 = DecimalNumber(1.6, color = RED,num_decimal_places=1).scale(0.7)
            #intro6 = TextMobject("children per family").scale(0.7)

        intro4.shift(2.8*UP + 0.7*LEFT)
        intro5.next_to(intro4,RIGHT)
        intro6.next_to(intro5,RIGHT)

        fert_rate_intro = VGroup(intro4,intro5,intro6)
        self.play(Write(fert_rate_intro),run_time = 2)
        self.wait()

        #introduce life expectancy
        if mode == "chinese":
            intro7 = TextMobject("人均寿命:").scale(0.7)
            intro8 = DecimalNumber(76.9,color = RED,num_decimal_places=1).scale(0.7)
            intro9 = TextMobject("岁").scale(0.7)

        else:
            intro7 = TextMobject("Average Life Expectancy is").scale(0.7)
            intro8 = DecimalNumber(76.3, color = RED,num_decimal_places=1).scale(0.7)
            intro9 = TextMobject("years").scale(0.7)

        intro7.shift(2.2*UP + 0.7*LEFT)
        intro8.next_to(intro7,RIGHT)
        intro9.next_to(intro8,RIGHT)

        life_expect_intro = VGroup(intro7,intro8,intro9)
        self.play(Write(life_expect_intro),run_time = 2)
        self.wait()     

        #move china to the left
        chinaG = VGroup(CN_name,life_expect_intro,fert_rate_intro,pop_intro)
        self.play(
            AnimationGroup(
                ApplyMethod(chinaG.shift,3.2*LEFT),
                ApplyMethod(chinamap.shift,3.2*LEFT)
                ),
            run_time = 1.5
            )


        #introducing USA:
        usamap = SVGMobject(file_name = USA_pic_dir,fill_opacity = 0.7, fill_color = BLUE).scale(2.5)
        usamap.shift(1*DOWN+3.2*RIGHT)

        #show USA map
        if mode == "chinese":
            USA_name = TextMobject("美国",color = BLUE)
        else:
            USA_name = TextMobject("USA",color = BLUE)

        USA_name.shift(3.5*DOWN+0.3*RIGHT+3.2*RIGHT)

        self.play(
            AnimationGroup(
                FadeIn(usamap),
                Write(USA_name)),
                run_time = 1
                )

        self.wait(2)
        
        #introduce population
        if mode == "chinese":
            intro10 = TextMobject("总人口数:").scale(0.7)
            intro11 = DecimalNumber(3.3,color = BLUE,num_decimal_places=1).scale(0.7)
            intro12 = TextMobject("亿").scale(0.7)

        else:
            intro10 = TextMobject("Population:").scale(0.7)
            intro11 = DecimalNumber(0.3,color = BLUE,num_decimal_places=1).scale(0.7)
            intro12 = TextMobject("billion").scale(0.7)

        intro10.shift(3.4*UP + 0.7*LEFT + 3.2*RIGHT)
        intro11.next_to(intro10,RIGHT)
        intro12.next_to(intro11,RIGHT)
        pop_intro_usa = VGroup(intro10,intro11,intro12)

        self.play(Write(pop_intro_usa),run_time = 2)
        self.wait()

        #introduce fertality rate
        if mode == "chinese":
            intro13 = TextMobject("每户孩子数:").scale(0.7)
            intro14 = DecimalNumber(1.9,color = BLUE,num_decimal_places=1).scale(0.7)
            intro15 = TextMobject("个").scale(0.7)

        else:
            intro13 = TextMobject("There are").scale(0.7)
            intro14 = DecimalNumber(1.9, color = BLUE,num_decimal_places=1).scale(0.7)
            intro15 = TextMobject("children per family").scale(0.7)

        intro13.shift(2.8*UP + 0.7*LEFT+ 3.2*RIGHT)
        intro14.next_to(intro13,RIGHT)
        intro15.next_to(intro14,RIGHT)

        fert_rate_intro_usa = VGroup(intro13,intro14,intro15)
        self.play(Write(fert_rate_intro_usa),run_time = 2)
        self.wait()

        #introduce life expectancy
        if mode == "chinese":
            intro16 = TextMobject("人均寿命:").scale(0.7)
            intro17 = DecimalNumber(79.1,color = BLUE,num_decimal_places=1).scale(0.7)
            intro18 = TextMobject("岁").scale(0.7)

        else:
            intro16 = TextMobject("Average Life Expectancy is").scale(0.7)
            intro17 = DecimalNumber(79.1, color = BLUE,num_decimal_places=1).scale(0.7)
            intro18 = TextMobject("years").scale(0.7)

        intro16.shift(2.2*UP + 0.7*LEFT+ 3.2*RIGHT)
        intro17.next_to(intro16,RIGHT)
        intro18.next_to(intro17,RIGHT)

        life_expect_intro_usa = VGroup(intro16,intro17,intro18)
        self.play(Write(life_expect_intro_usa),run_time = 2)
        self.wait(2)     
        
        usaG = VGroup(USA_name,life_expect_intro_usa,fert_rate_intro_usa,pop_intro_usa)

        #create the contry circle and transform the map to contry circle
        china = Contry("China")
        china.fill_data_and_set_the_circle(years=2018,color=RED,switch_on = False, show_CN_pop_lable = False)
        china.shape.move_to(chinamap.get_center())

        usa = Contry("United States")
        usa.fill_data_and_set_the_circle(years=2018,color=BLUE,switch_on = False, show_CN_pop_lable = False)
        usa.shape.move_to(usamap.get_center())

        
        self.play(
            AnimationGroup(
                ReplacementTransform(chinamap,china.shape),
                ReplacementTransform(usamap,usa.shape),
                run_time = 3
                )
            )
        
        #self.play(FadeOut(VGroup(chinamap,usamap)))#temp
        #self.play(FadeOut(VGroup(china.shape,usa.shape)))#temp

        self.wait(2)
        
        #scale the circe and change the population:

        original_radius_cn = get_norm(china.shape.get_center()-china.shape.points[0])
        original_radius_usa = get_norm(usa.shape.get_center()-usa.shape.points[0])
        if mode == "chinese":
            update_value_cn = 13.90
            update_value_usa = 3.27
        else:
            update_value_cn = 1.39
            update_value_usa = 0.32

        intro2.add_updater(
            lambda d: d.set_value(
                (update_value_cn*np.square(get_norm(china.shape.get_center()-china.shape.points[0])/original_radius_cn))
                )
            )        

        intro11.add_updater(
            lambda d: d.set_value(
                (update_value_usa*np.square(get_norm(usa.shape.get_center()-usa.shape.points[0])/original_radius_usa))
                )
            )

        self.play(
            AnimationGroup(
                ApplyMethod(china.shape.scale,2),
                ApplyMethod(usa.shape.scale,2)
                ),
            run_time = 2
            )

        self.wait(2)

        self.play(
            AnimationGroup(
                ApplyMethod(china.shape.scale,0.5),
                ApplyMethod(usa.shape.scale,0.5)
                ),
            run_time = 2
            )

        self.wait(2)
        
        # create the axes:
        axes = Axes(
            x_min = xmin,
            x_max = xmax,
            y_min = ymin,
            y_max = ymax,
            x_tick_frequency = 10,
            x_axis_config = {"tick_frequency":10,"leftmost_tick": 10,},
            y_axis_config = {"label_direction":LEFT},
            )
        axes.x_axis.move_to(ORIGIN,aligned_edge=LEFT)
        axes.y_axis.move_to(ORIGIN,aligned_edge=DOWN)
        axes.x_axis.stretch_about_point(x_scale_factor, 0, ORIGIN)
        axes.y_axis.stretch_about_point(y_scale_factor, 1, ORIGIN)
        axes.shift(NEWORIGIN)        

        for number in range(10,100,10):
            axes.x_axis.add_numbers(number)
        for number in range(1,10):
            axes.y_axis.add_numbers(number)        
        
        self.play(
            AnimationGroup(
                ShowCreation(axes),
                FadeOut(VGroup(CN_name,USA_name))
                ),
            run_time = 5
            )

        self.wait(2)

        y_axis_label_text = TextMobject("生育率").scale(0.6)
        y_axis_label_text.next_to(axes.y_axis.number_to_point(9), RIGHT+UP)

        x_axis_label_text = TextMobject("人均寿命").scale(0.6)
        x_axis_label_text.next_to(axes.x_axis.number_to_point(95), UP)
        self.play(Write(y_axis_label_text),Write(x_axis_label_text),run_time = 3)

        
        # move circle to the position on axes
        target_point_cn = china.get_transfromed_fertandlife_point(year_lable.get_value())#target_point_in_2018
        target_point_usa = usa.get_transfromed_fertandlife_point(year_lable.get_value())#target_point_in_2018
        
        self.play(
            AnimationGroup(
                ApplyMethod(china.shape.shift,target_point_cn - china.shape.get_center()),
                ApplyMethod(usa.shape.shift,target_point_usa - usa.shape.get_center())
                ),
            run_time = 3
            )

        self.wait()
        
        # create dots and lines to keep track of the value
        dot_cn = Dot(color = RED,radius = 0.03)
        dot_usa = Dot(color = BLUE,radius = 0.03)
        dot_cn.move_to(china.shape.get_center())
        dot_usa.move_to(usa.shape.get_center())
        self.play(FadeIn(VGroup(dot_cn,dot_usa)),run_time = 1)
        
        vline_cn = Line(
            [target_point_cn[0],NEWORIGIN[1],0],
            target_point_cn,
            stroke_width = 2,
            stroke_color = RED
        )
        hline_cn = Line(
            [NEWORIGIN[0],target_point_cn[1],0],
            target_point_cn,
            stroke_width = 2,
            stroke_color = RED
        )

        vline_usa = Line(
            [target_point_usa[0],NEWORIGIN[1],0],
            target_point_usa,
            stroke_width = 2,
            stroke_color = BLUE
        )
        hline_usa = Line(
            [NEWORIGIN[0],target_point_usa[1],0],
            target_point_usa,
            stroke_width = 2,
            stroke_color = BLUE
        )

        self.play(ShowCreation(VGroup(vline_usa,hline_usa,vline_cn,hline_cn)),run_time = 1.5)

        vline_cn.add_updater(lambda v: v.set_points_as_corners([[dot_cn.get_center()[0],NEWORIGIN[1],0], dot_cn.get_center()]))
        hline_cn.add_updater(lambda h: h.set_points_as_corners([[NEWORIGIN[0],dot_cn.get_center()[1],0], dot_cn.get_center()]))
        vline_usa.add_updater(lambda v: v.set_points_as_corners([[dot_usa.get_center()[0],NEWORIGIN[1],0], dot_usa.get_center()]))
        hline_usa.add_updater(lambda h: h.set_points_as_corners([[NEWORIGIN[0],dot_usa.get_center()[1],0], dot_usa.get_center()]))
        self.add(vline_cn,hline_cn,dot_usa,dot_cn,vline_usa,hline_usa)
        
        self.wait(2)

        #create coordinates lables
        china.create_data_coordinate_lable(2018)
        CN_coor_lables = VGroup(china.data_coordinate_lable,china.data_x_lable,china.data_y_lable)
        CN_coor_lables.shift(2.75*LEFT + 0.5*UP)

        self.play(
            ShowCreation(china.data_coordinate_lable),
            TransformFromCopy(intro8,china.data_x_lable),
            TransformFromCopy(intro5,china.data_y_lable),
            run_time = 2          
            )

        usa.create_data_coordinate_lable(2018,lable_color = BLUE)
        USA_coor_lables = VGroup(usa.data_coordinate_lable,usa.data_x_lable,usa.data_y_lable)
        USA_coor_lables.shift(0.35*LEFT)

        self.play(
            ShowCreation(usa.data_coordinate_lable),
            TransformFromCopy(intro17,usa.data_x_lable),
            TransformFromCopy(intro14,usa.data_y_lable),
            run_time = 2          
            )

        self.wait(2)


        #TODO-----: redundant
        china.contry_name = TextMobject("1")
        usa.contry_name = TextMobject("2")
        #---------
        #print(hasattr(china,'data_coordinate_lable'))

        self.play(FadeOut(VGroup(life_expect_intro_usa,fert_rate_intro_usa,pop_intro_usa,life_expect_intro,fert_rate_intro,pop_intro)))
        
        #area demo
        self.wait(0.5)
        text1 = TextMobject("寿命长", color =  RED)
        text2 = TextMobject("小家庭", color =  RED)
        text2.next_to(china.shape,UP)
        text1.next_to(text2,UP)

        self.play(Write(VGroup(text1,text2)),run_time = 2)
        self.wait(6)

        text3 = TextMobject("寿命短", color =  BLUE)
        text4 = TextMobject("大家庭", color =  BLUE)
        text3.next_to(y_axis_label_text,DOWN)
        text3.shift(0.3*RIGHT)
        text4.next_to(text3,DOWN)       

        self.play(Write(VGroup(text3,text4)),run_time = 2)
        self.wait(3)
        self.play(FadeOut(VGroup(text1,text2,text3,text4)),run_time = 1)

        shift_vect_cn = china.get_transfromed_fertandlife_point(1800) - china.shape.get_center()
        shift_vect_usa = usa.get_transfromed_fertandlife_point(1800) - usa.shape.get_center()
        self.play(                
            china.update_circlelable_by_year_animation(1800),
            usa.update_circlelable_by_year_animation(1800),
            china.update_circle_by_year_animation(1800,show_track=False),
            usa.update_circle_by_year_animation(1800,show_track=False),                
            ApplyMethod(VGroup(china.data_coordinate_lable,dot_cn).shift,shift_vect_cn),
            ApplyMethod(VGroup(usa.data_coordinate_lable,dot_usa).shift,shift_vect_usa),
            year_lable.set_value,1800,
            run_time = 3
            )
        self.wait(9)


        for new_year in [1825,1850,1875,1900,1920,1940,1950,1960,1970,1975,1980,2008,2015,2018]:
            shift_vect_cn = china.get_transfromed_fertandlife_point(new_year) - china.shape.get_center()
            shift_vect_usa = usa.get_transfromed_fertandlife_point(new_year) - usa.shape.get_center()
            self.play(                
                china.update_circlelable_by_year_animation(new_year),
                usa.update_circlelable_by_year_animation(new_year),
                china.update_circle_by_year_animation(new_year,show_track=False),
                usa.update_circle_by_year_animation(new_year,show_track=False),                
                ApplyMethod(VGroup(china.data_coordinate_lable,dot_cn).shift,shift_vect_cn),
                ApplyMethod(VGroup(usa.data_coordinate_lable,dot_usa).shift,shift_vect_usa),
                year_lable.set_value,new_year,
                run_time = 2
                )
            #print(china.data_x_lable.get_value(),usa.data_x_lable.get_value())
            self.wait(1)        

        #3:11;16
        self.wait(2)
        #3:13;16
        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)

        self.wait()
