from argparse import ArgumentParser
import emoji
import sys

def get_emoji(i,status):
    animals = [':dog:', ':cat:', ':mouse:', ':hamster:', ':rabbit:', ':wolf:', ':frog:', ':tiger:', ':koala:', ':bear:', ':pig:', ':pig_nose:', ':cow:', ':boar:', ':monkey_face:', ':monkey:', ':horse:', ':racehorse:', ':camel:', ':sheep:', ':elephant:', ':panda_face:', ':snake:', ':bird:', ':baby_chick:', ':hatched_chick:', ':hatching_chick:', ':chicken:', ':penguin:', ':turtle:', ':bug:', ':honeybee:', ':ant:', ':beetle:', ':snail:', ':octopus:', ':tropical_fish:', ':fish:', ':whale:', ':whale2:', ':dolphin:', ':cow2:', ':ram:', ':rat:', ':water_buffalo:', ':tiger2:', ':rabbit2:', ':dragon:', ':goat:', ':rooster:', ':dog2:', ':pig2:', ':mouse2:', ':ox:', ':dragon_face:', ':blowfish:', ':crocodile:', ':dromedary_camel:', ':leopard:', ':cat2:', ':poodle:', ':paw_prints:', ':bouquet:', ':cherry_blossom:', ':tulip:', ':four_leaf_clover:', ':rose:', ':sunflower:', ':hibiscus:', ':maple_leaf:', ':leaves:', ':fallen_leaf:', ':herb:', ':ear_of_rice:', ':mushroom:', ':cactus:', ':palm_tree:', ':evergreen_tree:', ':deciduous_tree:', ':chestnut:', ':seedling:', ':blossom:', ':globe_with_meridians:', ':sun_with_face:', ':full_moon_with_face:', ':new_moon_with_face:', ':new_moon:', ':waxing_crescent_moon:', ':first_quarter_moon:', ':waxing_gibbous_moon:', ':full_moon:', ':waning_gibbous_moon:', ':last_quarter_moon:', ':waning_crescent_moon:', ':last_quarter_moon_with_face:', ':first_quarter_moon_with_face:', ':moon:', ':earth_africa:', ':earth_americas:', ':earth_asia:', ':volcano:', ':milky_way:', ':partly_sunny:', ':octocat:', ':shipit:', ':squirrel:']
    #TODO add CDFR people list
    if status == 1:
        return animals[i]
    else:
        return animals[i+1]
 

 