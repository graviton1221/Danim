from Danim.Contry import *
from Danim.Distribution import LogscaleNumberLine

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

class MoreComparison(Scene):

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
            leftmost_tick = 10
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

        #6:33;10
        self.play(ShowCreation(axes,run_time = 3.5))


        y_axis_label_text = TextMobject("人均寿命").scale(0.6)
        y_axis_label_text.next_to(axes.y_axis.number_to_point(95), RIGHT+UP)

        x_axis_label_text = TextMobject("人均GDP").scale(0.6)
        x_axis_label_text.next_to(axes.x_axis.number_to_point(9.5), UP)
        self.play(Write(y_axis_label_text),Write(x_axis_label_text),run_time = 2)
        self.wait(4)

        #create year lable:
        year_lable = Integer(1800,group_with_commas = False,color = TEAL_E).scale(1.5)
        year_lable.to_edge(UR)
        self.play(GrowFromCenter(year_lable),run_time =1)
        #print(axes.x_axis.numbers)
        
        Text1 = TextMobject("贫穷和疾苦", color = BLUE).move_to(2.5*DOWN+4*LEFT)
        Text2 = TextMobject("富有和健康", color = RED).move_to(2.5*UP+4*RIGHT)
        self.play(Write(Text1),run_time = 2)
        self.wait(3)
        self.play(Write(Text2),run_time = 2)
        self.wait(3)

        self.play(FadeOut(VGroup(Text1,Text2)))

        self.wait()
        Text3 = TextMobject("GDP单位为2011年物价水平")
        Text3.shift(UP)
        Text4 = TextMobject("1国际元约为2011年的3.6元人民币")
        Text5 = TextMobject("1国际元约为2018年的4元人民币")
        Text4.next_to(Text3,DOWN)
        Text5.next_to(Text4,DOWN)

        #6:55;20
        self.play(Write(VGroup(Text3,Text4,Text5)),run_time = 3)
        #6:58;20
        self.wait(7)
        #7:05;20
        self.play(FadeOut(VGroup(Text3,Text4,Text5)))
        #bubble creation animation
        #create add all areas circles

        area_rect = []
        area_rect_lable = []
        areas = []
        for i,area in enumerate(THE_WHOLE_WORLD):

            areas.append(Area(area,show_CN_name = True))
            area_rect.append(Rectangle(height = 0.2, width = 0.5,color = AREA_COLOR_MAP[i],fill_opacity = 1))
            
            if i == 0:
                area_rect[i].next_to(year_lable,6*DOWN)

            else:
                area_rect[i].next_to(area_rect[i-1],DOWN)
            area_rect_lable.append(TextMobject(CH_THE_WHOLE_WORLD[i]).scale(0.4))
            area_rect_lable[i].next_to(area_rect[i],LEFT)

            #notice: before run this function 
            #change get_both_fertandlife_point() 
            #function in Contry.py to Version 2
            areas[i].generate_all_contry_circles(
                years_date=1800,
                COLORMAT = [AREA_COLOR_MAP[i]],
                if_switch_on =True,
                Axes = axes,
                sort_by_axes =True
                )
            self.play(*areas[i].get_creation_animation(sort_by_axes= True),
                GrowFromCenter(area_rect[i]),
                Write(area_rect_lable[i])
                )
            
            self.wait(2)
            self.play(AnimationGroup(*areas[i].transform_animations,lag_ratio = 0.1))

        self.wait()

        for i,contry in enumerate(areas[3].contry_list):
            if contry.name == "United States":
                US_index = i
        for i,contry in enumerate(areas[1].contry_list):
            if contry.name == "Iran":
                IRAN_index = i
            elif contry.name == "China":
                CN_index = i
            elif contry.name == "India":    
                India_index = i
            elif contry.name == "Japan":
                JP_index = i
                japan = contry

        #Stage1: 1800 - 1938

        TIME_TOTOL = 55 # 2.5years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1801,1938,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1801,1938,1))

        for new_year in range(1801,1938,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:

                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
            

            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        #stage2: pause at 1938

        JP_lable = TextMobject("日本",color = RED).scale(0.1)
        JP_lable.move_to(japan.shape.get_center())
        JP_lable1 = TextMobject("日本",color = RED).scale(0.8)
        JP_lable1.next_to(japan.shape,2*UP)

        self.play(FadeIn(JP_lable),run_time = 0.5)
        self.play(
            AnimationGroup(
                ReplacementTransform(
                    JP_lable,
                    JP_lable1
                    ),
                WiggleOutThenIn(
                    japan.shape,
                    scale_value = 1.5
                    ),
                run_time = 1.5
                )
            )
        self.wait()
        self.play(FadeOut(JP_lable1))

        #Stage3: 1938 - 1948

        TIME_TOTOL = 4 # 2.5years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1938,1949,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1938,1949,1))

        for new_year in range(1938,1949,1):
            area_animation = []
            contry_name_anim = []
            for area in areas:

                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters
            

            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        #8:53;02
        self.wait(8.08)
        #9:01:11
        #stage 4: pause at 1948


        #HIGHTLIGHT US:
        US_lable = TextMobject("美国",color = BLUE).scale(0.1)
        US_lable.move_to(areas[3].contry_list[US_index].shape.get_center())
        US_lable1 = TextMobject("美国",color = BLUE).scale(0.8)
        US_lable1.next_to(areas[3].contry_list[US_index].shape,UP)

        self.play(FadeIn(US_lable),run_time = 0.5)
        self.play(
            AnimationGroup(
                ReplacementTransform(
                    US_lable,
                    US_lable1
                    ),
                WiggleOutThenIn(
                    areas[3].contry_list[US_index].shape,
                    scale_value = 1.5
                    ),
                run_time = 1.5
                )
            )
        self.wait()

        lables = []
        lables1 = []
        for i,index in enumerate([IRAN_index,CN_index,India_index]):
            lables.append(TextMobject(online_translation(areas[1].contry_list[index].name),color = RED).scale(0.1))
            lables[i].move_to(areas[1].contry_list[index].shape.get_center())
            lables1.append(TextMobject(online_translation(areas[1].contry_list[index].name),color = RED).scale(0.8))
            lables1[i].next_to(areas[1].contry_list[index].shape,DOWN)

            self.play(FadeIn(lables[i]),run_time = 0.2)
            self.play(
                AnimationGroup(
                    ReplacementTransform(lables[i],lables1[i]),
                    WiggleOutThenIn(areas[1].contry_list[index].shape,scale_value = 1.5,run_time = 3),
                    run_time = 2))
            self.wait()
        
        #09:12;27
        lables1.append(US_lable1)
        lables = VGroup()
        for lable in lables1:
            lables.add(lable)
        self.wait()
        #09:13;27
        self.play(FadeOut(lables))
        self.wait()

        #stage 5: 1949-2018

        TIME_TOTOL = 30 # 2.5years per sec

        transfer_time = 0.7*TIME_TOTOL/len(range(1949,2019,1))
        wait_time = 0.3*TIME_TOTOL/len(range(1949,2019,1))

        for new_year in range(1949,2019,1):
            area_animation = []
            contry_name_anim = []

            for area in areas:

                area_animation += area.update_area_contryname_by_year_animation(new_year)
                area_animation += area.update_area_circles_by_year_animation(new_year)
                # SEQUENCE matters


            self.play(
                *area_animation,
                year_lable.set_value,new_year,
                run_time = transfer_time
                )
            self.wait(wait_time)

        #stage 6: pause at 2018:
        #09:44;12
        self.wait(5)
        #09:49.12
        #high light Qatar and NK and Luxembourg
        for area in areas:
            for contry in area.contry_list:
                if contry.name == "North Korea":
                    north_korea = contry
                elif contry.name == "Luxembourg":
                    luxembourg = contry
                elif contry.name == "Qatar":
                    qatar = contry
                elif contry.name == "China":
                    china = contry
                elif contry.name == "Congo, Dem. Rep.":
                    congo = contry

        lables = []
        lables1 = []
        colors = [YELLOW,RED,GREEN,RED]
        for i,contry in enumerate([luxembourg,qatar,congo,north_korea]):
            lables.append(TextMobject(online_translation(contry.name),color = colors[i]).scale(0.1))
            lables[i].move_to(contry.shape.get_center())
            lables1.append(TextMobject(online_translation(contry.name),color = colors[i]).scale(0.8))
            
            if i == 1:
                lables1[i].next_to(contry.shape,DOWN)
            else:
                lables1[i].next_to(contry.shape,UP)

            self.play(FadeIn(lables[i]),run_time = 0.2)
            self.play(
                AnimationGroup(
                    ReplacementTransform(lables[i],lables1[i]),
                    WiggleOutThenIn(contry.shape,scale_value = 1.5,run_time = 2),
                    run_time = 2))
            self.wait(0.5)
                
        lables = VGroup()
        for lable in lables1:
            lables.add(lable)
        self.play(FadeOut(lables))
        #10:00;27
        self.wait(5)


        #HIGHLIGHT China
        lables = TextMobject("中国", color = RED).scale(0.1)
        lables1 = TextMobject("中国", color = RED).scale(0.8)
        lables.move_to(china.shape.get_center())
        lables1.next_to(china.shape,UP)

        self.play(FadeIn(lables),run_time = 0.2)
        self.play(
            AnimationGroup(
                ReplacementTransform(lables,lables1),
                WiggleOutThenIn(china.shape,scale_value = 1.5,run_time = 2),
                run_time = 2))
        #10:07;11
        self.wait(8.16)
        #10:15;27
        #self.play(FadeOut(lables1))


        '''
        #end Scene and fadeout everything excpet the logo
        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)        
        '''
