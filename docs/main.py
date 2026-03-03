#Power Out

#Leikjaspilun
#Spilið inniheldur 5 borgir og af þeim eru 4 fyrir leikmenn. Leikmenn ýta á takkann í miðjunni til þess að komast að því hvaða lit af reit þeir mega taka næst en í hver tvö skipti sem ýtt er á takkann dettur rafmagnið út í einni handahófskenndri borg (ljósið í henni slokknar). Leikmenn geta notað einn reit af þeim lit sem var birtur á skjáinn til þess að reyna að ná aftur í rafmagn. Þetta heldur áfram þar til allar borgir hafa reynt að slökkva einu sinni á sér, og ef leikmenn hafa ekki tengt a.m.k. eina borg við aðalborgina þá tapa þeir. Eftir þetta reyna leikmenn að ná að tengja hinar borgirnar í aðalborgina (í miðjunni) til þess að ná aftur rafmagni í allar borgirnar. Ef rafmagn kemst á allar borgir vinna leikmenn en ef þeir ná því ekki (t.d. ef borðið flækist og réttir reitir komast ekki fyrir) þá tapa þeir.

#Spilareglur
#- Leikmenn eiga að vinna saman.
#- Hver og einn leikmaður getur gert einu sinni í einu. Leikmaður ýtir á takkann í miðjunni og notar reit af þeim liti.
#- Ef slokknar á öllum borgum án þess að leikmenn nái að tengja eina við rafmagn tapa þeir. Sömuleiðis ef þeir geta ekki lengur tengt einhverja borg.
#- Ef leikmenn ná að kveikja aftur á öllum borgum vinna þeir.
#- Reitir eru fastir á borði en þó má taka þá upp til þess að lagfæra (ljós slokknar ekki ef hún hefur áður verið tengd í aðalborgina).


#Söfn
from machine import Pin, SoftI2C
from I2C_LCD import I2cLcd
from neopixel import NeoPixel
from buzzer_music import music
import time
import random

#Hljóð
win_sfx = '0 D4 1 14;1 E4 1 14;2 F#4 1 14;3 G#4 1 14;4 B4 1 14;5 E5 2 14;8 A4 2 14;11 D4 1 14;12 E4 1 14;13 F#4 1 14;14 G#4 1 14;15 A#4 1 14;16 F#5 2 14;19 C#4 2 14;22 C#4 1 14;23 D#4 1 14;24 F4 1 14;25 A#4 1 14;26 A#4 1 14;28 D5 1 14;30 F#5 1 14;32 F#5 1 14;34 A#5 2 14'
lose_sfx = '0 F5 1 43;0 D5 1 43;0 A#4 1 43;1 C#5 1 43;1 A#4 1 43;1 F#4 1 43;2 D4 1 43;2 F#4 1 43;2 A4 1 43;3 A4 1 43;2 A5 1 43;3 D4 1 43;4 D4 1 43;4 F4 1 43;4 A4 1 43;6 D4 1 43;6 F4 1 43;6 A4 1 43;7 C#5 1 43;7 A4 1 43;7 F#4 1 43;8 A#4 4 43;8 G4 4 43;8 D#4 4 43;12 F#4 3 43;12 D#4 3 43;12 B3 3 43;15 D4 4 43;15 B3 4 43;15 G3 4 43'
intro_sfx = '0 C#6 4 43;0.75 F#6 3.75 43;1.5 G#6 3.5 43;2 C#7 8 43;2.75 F7 9.25 43;16 A#4 1 32;19 A4 1 32;20.5 F4 1 32;22.5 D5 1 32;24 C5 4 32;21.5 G4 1 32;16 D#4 1 5;19 D#4 1 5;20.5 D#4 1 5;24 C4 4 5;22 G3 1 5;16 A#5 1 9;19 A5 1 9;20.5 F5 1 9;21.5 G5 1 9;22.5 D5 1 9;24 C5 4 9;24 C6 1 12;23 D6 1 12;16 A#5 1 12;19 A5 1 12;20.5 F5 1 12;21.5 G5 1 12;22.5 D5 1 12;16 A#5 1 20;19 A5 1 20;20.5 F5 1 20;21.5 G5 1 20;24 C7 0.5 26'
button_sfx = '0 F7 1 60;0 D7 1 21;0 F#7 1 21'

#Algeng ljós
neo_brightness = 50
neo_off = [0, 0, 0]
neo_color = [neo_brightness, 0, 0]

#Pinnar og breytur fyrir þá
i2c = SoftI2C(scl=Pin(9), sda=Pin(8), freq=400000)
lcd = I2cLcd(i2c, 39, 2, 16)
button = Pin(11, Pin.IN, Pin.PULL_UP)
neo = NeoPixel(Pin(5, Pin.OUT), 16)
leds = {
    "Yellow": {"pin": 0, "connected": False, "color": [neo_brightness, neo_brightness, 0], "wire": Pin(12, Pin.IN, Pin.PULL_UP), "state_before": 1},
    "Red": {"pin": 1, "connected": False, "color": [0, neo_brightness, 0], "wire": Pin(10, Pin.IN, Pin.PULL_UP), "state_before": 1},
    "Green": {"pin": 2, "connected": False, "color": [neo_brightness, 0, 0], "wire": Pin(46, Pin.IN, Pin.PULL_UP), "state_before": 1},
    "Blue": {"pin": 3, "connected": False, "color": [0, 0, neo_brightness], "wire": Pin(18, Pin.IN, Pin.PULL_UP), "state_before": 1},
}
rgb_leds = NeoPixel(Pin(21, Pin.OUT), 4)

button_state_before = 1
on = True
button_presses = 0

colors_reconnected = []
colors = ["Yellow", "Red", "Green", "Blue"]

#Fall sem sér um upphafs ljósasýninguna
def light_show():
    random_color = random.choice(colors)
    rgb_led = leds[random_color]["pin"]
    rgb_leds[rgb_led] = leds[random_color]["color"]
    rgb_leds.write()
        
    neo[random.randint(0, 15)] = leds[random_color]["color"]
    neo.write()
         
    time.sleep(0.04)
        
    rgb_leds.fill(neo_off)
    rgb_leds.write()
        
    neo.fill(neo_off)
    neo.write()

#Fall sem sér um ljósasýninguna þegar maður vinnur eða tapar
def win_or_lose_show(win):
    rgb_leds[random.randint(0, 3)] = win and neo_color or [0, neo_brightness, 0]
    rgb_leds.write()
    
    neo[random.randint(0, 15)] = neo_color
    neo.write()
    
    time.sleep(0.04)
    
    rgb_leds.fill(neo_off)
    rgb_leds.write()
    
    neo.fill(neo_off)
    neo.write()

#Fall sem sér um að byrja leikinn upp á nýtt
def reset_game():
    global colors, colors_reconnected, button_presses, button_state_before, on
    colors = ["Yellow", "Red", "Green", "Blue"]
    colors_reconnected = []
    button_presses = 0
    button_state_before = 1
    for name in leds:
        leds[name]["connected"] = False
        leds[name]["state_before"] = 1
    rgb_leds.fill(neo_off)
    rgb_leds.write()
    time.sleep(0.05)
    for led_name in leds:
        rgb_led = leds[led_name]["pin"]
        rgb_leds[rgb_led] = leds[led_name]["color"]
    rgb_leds.write()
    neo.fill(neo_color)
    neo.write()
    
    on = True

try:
    #Spila upphafs lagið og setja leikinn upp
    intro_song = music(intro_sfx, pins=[Pin(7)], looping=False)
    while not intro_song.stopped:
        intro_song.tick()
        light_show()
        
    reset_game()

    while True:
        while on:
            #Kíkja hvaða vírar eru tengdir
            for led_name in leds:
                wire = leds[led_name]["wire"]
                if wire.value() == 0 and leds[led_name]["state_before"] == 1:
                    leds[led_name]["state_before"] = wire.value()
                    colors.append(led_name) if led_name not in colors else None
                    colors_reconnected.append(led_name)
                    leds[led_name]["connected"] = True
                    
                    #Kveikja ljós þeirra víra sem eru tengdir
                    rgb_leds[leds[led_name]["pin"]] = leds[led_name]["color"]
                    rgb_leds.write()
                    
                    #Ef allir eru tengdir þá á að spila vinningslagið og vinnings ljósasýninguna ásamt því að skrifa "You won!" á skjáinn
                    if len(colors_reconnected) == 4:
                        lcd.clear()
                        lcd.putstr("You won!")
                        on = False
                        win_song = music(win_sfx, pins=[Pin(7)], looping=False)
                        while not win_song.stopped:
                            win_song.tick()
                            win_or_lose_show(True)
                        break

            button_state = button.value()
            
            #Kíkja hvort ýtt var á takkann
            if button_state == 0 and button_state_before == 1:
                #Spila takkahljóðið
                button_song = music(button_sfx, pins=[Pin(7)], looping=False)
                while not button_song.stopped:
                    button_song.tick()
                
                button_presses += 1
                
                #Breyta textanum á skjánum til þess að segja hvaða lit maður á að taka ef ýtt var á takkann
                lcd.clear()
                if len(colors) > 0:
                    random_color = random.choice(colors)
                    lcd.putstr(f"Take {random_color}!")

                if button_presses % 2 == 0 and len(colors) > 0:
                    random_color = random.choice(colors)
                    rgb_led = leds[random_color]["pin"]
                    
                    #Slökkva á ljósi ef það er eitthvað ótengt ljós og það er búið að ýta tvisvar á takkann.
                    if not leds[random_color]["connected"]:
                        rgb_leds[rgb_led] = neo_off
                        rgb_leds.write()
                        try:
                            colors.remove(random_color)
                        except ValueError:
                            pass
                        
                        #Skrifa "Game over" ef slökkt er á öllum ljósum og ekkert hefur verið tengt
                        if len(colors) == 0:
                            lcd.clear()
                            lcd.putstr("Game over.")
                            on = False
                            lose_song = music(lose_sfx, pins=[Pin(7)], looping=False)
                            while not lose_song.stopped:
                                lose_song.tick()
                                win_or_lose_show(False)
                            break

            button_state_before = button_state
            time.sleep(0.01)

        #Skrifa "Click twice to" á fyrstu línu og svo "replay" á seinni línu ef leikurinn er búinn
        lcd.clear()
        lcd.putstr("Click twice to")
        try:
            lcd.move_to(0, 1)
        except Exception:
            pass
        lcd.putstr("replay")

        replay_presses = 0
        last_state = button.value()

        #Gá hvort búin sé að ýta á takkann tvisvar til þess að byrja upp á nýtt
        while replay_presses < 2:
            state = button.value()
            if state == 0 and last_state == 1:
                time.sleep(0.05)
                replay_presses += 1
                
                #Spila takkahljóðið
                fb = music(button_sfx, pins=[Pin(7)], looping=False)
                while not fb.stopped:
                    fb.tick()
            last_state = state
            time.sleep(0.05)

        reset_game()

finally:
    #Slökkva á öllu þegar slökkt er a leiknum
    lcd.clear()
    lcd.backlight_off()
    neo.fill(neo_off)
    neo.write()
    
    rgb_leds.fill(neo_off)
    rgb_leds.write()
