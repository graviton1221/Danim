from big_ol_pile_of_manim_imports import *

hans_pic_dir = "Danim\\video1\\file\\HANS2.png"
developing_pic_dir = "Danim\\video1\\file\\rural.png"
developed_pic_dir = "Danim\\video1\\file\\city.png"
population_pic_dir = "Danim\\video1\\file\\population.png"
money_pic_dir = "Danim\\video1\\file\\money.png"

person_svg_dir = "Danim\\video1\\file\\person.svg"
family_svg_dir = "Danim\\video1\\file\\family.svg"
tomb_svg_dir = "Danim\\video1\\file\\tomb.svg"

mode = "chinese"

class LogoAndOpenning(Scene):
    def construct(self, mode = mode):
        
        #logotag
        logotag = TextMobject("引力子G @B站").scale(0.4)
        logotag.to_edge(DR)
        logotag.shift(0.4*DOWN+0.4*RIGHT)
        logotag.asdfi = 1# no use, for not fadeout in the end
        
        self.add(logotag)


        # create mobject for HR and adjust the position
        pic = ImageMobject(hans_pic_dir, image_mode = "L")
        
        pic.scale(2)
        pic.shift(1*UP)

        self.play(FadeIn(pic))

        if mode == "chinese":
            intro1 = TextMobject("谨以此视频纪念汉斯·罗斯林先生").scale(0.8)
            intro1.shift(1.5*DOWN)

            intro2 = TextMobject("(1948 - 2017)").scale(0.6)

            intro2.shift(2*DOWN)
        
        elif mode == "english":
            intro1 = TextMobject("In memory of Hans Rosling").scale(0.8)
            intro1.shift(1.5*DOWN)

            intro2 = TextMobject("(1948 - 2017)").scale(0.6)

            intro2.shift(2*DOWN)

        self.play(Write(VGroup(intro1,intro2)))
        self.wait(6.16)
        #8.16s
        self.play(
        	AnimationGroup(
        		FadeOut(VGroup(intro1,intro2)),
        		FadeOut(pic)))

        #introducing difference between developed contry and developing contry
        developing_country = ImageMobject(developing_pic_dir)
        developing_country.shift(3*LEFT + 2*UP)
        if mode == "chinese":
            developing_country_lable = TextMobject("发展中国家",color = RED)
        elif mode == "english":
            developing_country_lable = TexMobject("Developing Country",color = RED)
        developing_country_lable.next_to(developing_country,UP)

        developed_country = ImageMobject(developed_pic_dir)
        developed_country.shift(3*RIGHT + 2*UP)

        if mode == "chinese":
            developed_country_lable = TextMobject("发达国家",color = BLUE)
        elif mode == "english":
            developed_country_lable = TexMobject("Developed Country",color = BLUE)
        developed_country_lable.next_to(developed_country,UP)

        self.play(*[
            GrowFromCenter(developing_country),
            GrowFromCenter(developed_country),
            ],
            run_time = 2
            )
        #12.16s
        self.wait(1)
        #13.16
        self.play(*[
            Write(developing_country_lable),
            Write(developed_country_lable)
            ],
            run_time = 2
            )
        #15.16
        self.wait()
        #16.16

        #population question mark
        population = ImageMobject(population_pic_dir).scale(0.6)
        if mode == "chinese":
            population_lable = TextMobject("人均寿命").scale(0.6)
        elif mode == "english":
            population_lable = TextMobject("Life Expectancy").scale(0.6)
        question_mark1 = TexMobject("?").scale(0.6)

        population_lable.next_to(population,DOWN)
        question_mark1.next_to(population_lable,RIGHT)
        if mode == "english":
            question_mark1.shift(0.2*LEFT+0.04*UP)
        elif mode == "chinese":
            question_mark1.shift(0.2*LEFT)

        self.play(*[
            GrowFromCenter(population),
            Write(question_mark1),
            Write(population_lable)
            ],
            run_time = 3)
        self.wait()
        #20.16

        #money question mark
        money = ImageMobject(money_pic_dir).scale(0.6)
        if mode == "chinese":
            money_lable = TextMobject("财富").scale(0.6)
        elif mode == "english":
            money_lable = TextMobject("Wealth").scale(0.6)
        question_mark2 = TexMobject("?").scale(0.6)

        money.shift(2*DOWN)
        money_lable.next_to(money,DOWN)
        question_mark2.next_to(money_lable,RIGHT)
        if mode == "english":
            question_mark2.shift(0.2*LEFT+0.04*UP)
        elif mode == "chinese":
            question_mark2.shift(0.2*LEFT)

        self.play(*[
            GrowFromCenter(money),
            Write(question_mark2),
            Write(money_lable)
            ],
            run_time = 2)
        self.wait()
        #23.16

        self.play(*[
            FadeOut(VGroup(
                money_lable,
                question_mark2,
                question_mark1,
                population_lable)),
            FadeOut(money),
            FadeOut(population),
            ]
            )

        self.wait(7)
        # Show developing country has more kids and short life?
        family = SVGMobject(family_svg_dir).scale(0.5)
        family.shift(3*LEFT+0.2*UP)
        self.play(GrowFromCenter(family),run_time = 2)
        self.wait()

        developing_kids = VGroup()
        for i in range(8):
            kid = SVGMobject(person_svg_dir).scale(0.3)
            
            if i == 0:
                kid.shift(4.75*LEFT+2*DOWN)
                developing_kids.add(kid)
            else:
                kid.next_to(developing_kids)
                developing_kids.add(kid)

        arrow1 = Arrow([0,0,0],[0,-1,0],color = RED)
        arrow1.next_to(family,DOWN)
        arrow1.shift(0.2*DOWN)
        self.play(*[ShowCreation(developing_kids),GrowFromCenter(arrow1)],run_time = 2)
        self.wait(1)

        developing_toms = VGroup()
        animations = []
        for i,index in enumerate([0,2,5,7]):

            developing_toms.add(SVGMobject(tomb_svg_dir).scale(0.3))
            developing_toms.submobjects[i].move_to(developing_kids.submobjects[index].get_center())

            animations.append(
                AnimationGroup(
                    FadeOut(developing_kids.submobjects[index],run_time = 1.5),
                    FadeIn(developing_toms.submobjects[i],run_time = 1.5)
                    ,lag_ratio = 1
                    )
                )

        developing_lable1 = TextMobject("人均寿命较短",color = RED).scale(0.7)
        developing_lable1.next_to(developing_kids,DOWN)
        developing_lable2 = TextMobject("每户孩子数多",color = RED).scale(0.7)
        developing_lable2.next_to(developing_lable1,DOWN)        
        
        self.play(*animations)

        self.play(Write(VGroup(developing_lable1,developing_lable2)))
        self.wait()
        

        # Show developed country has less kids and longer life?
        family2 = SVGMobject(family_svg_dir).scale(0.5)
        family2.shift(3*RIGHT+0.2*UP)

        developed_kids = VGroup()
        for i in range(3):
            kid = SVGMobject(person_svg_dir).scale(0.3)
            
            if i == 0:
                kid.shift(2.5*RIGHT+2*DOWN)
                developed_kids.add(kid)
            else:
                kid.next_to(developed_kids)
                developed_kids.add(kid)

        arrow2 = Arrow([0,0,0],[0,-1,0],color = RED)
        arrow2.next_to(family2,DOWN)
        arrow2.shift(0.2*DOWN)        
        
        self.play(GrowFromCenter(family2),run_time = 1)
        self.wait()
        self.play(*[GrowFromCenter(arrow2),ShowCreation(developed_kids)],run_time = 1)
        self.wait(2)

        developed_toms = VGroup()
        animations = []
        for i,index in enumerate([0]):

            developed_toms.add(SVGMobject(tomb_svg_dir).scale(0.3))
            developed_toms.submobjects[i].move_to(developed_kids.submobjects[index].get_center())

            animations.append(
                AnimationGroup(
                    FadeOut(developed_kids.submobjects[index],run_time = 1.5),
                    FadeIn(developed_toms.submobjects[i],run_time = 1.5)
                    ,lag_ratio = 1
                    )
                )
        
        developed_lable1 = TextMobject("人均寿命较长",color = BLUE).scale(0.7)
        developed_lable1.next_to(developed_kids,DOWN)
        developed_lable2 = TextMobject("每户孩子数少",color = BLUE).scale(0.7)
        developed_lable2.next_to(developed_lable1,DOWN)

        self.play(*animations)

        self.play(Write(VGroup(developed_lable1,developed_lable2)))
        self.wait(2)

        question_mark3 = TexMobject("?",color = PURPLE).scale(3)

        self.play(GrowFromCenter(question_mark3))
        self.wait(2)
        animations = []
        for mob in self.mobjects:
            if isinstance(mob,Mobject) & (not hasattr(mob,"asdfi")):
                animations.append(FadeOut(mob))

        self.play(*animations)

        
