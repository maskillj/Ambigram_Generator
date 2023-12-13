from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import warnings
warnings.filterwarnings("ignore")

font_list = ['AbrilFatface-Regular.otf','AlexBrush-Regular.ttf','Aller_Bd.ttf','Aller_BdIt.ttf','Aller_It.ttf','Aller_Lt.ttf','Aller_LtIt.ttf','Aller_Rg.ttf','AllerDisplay.ttf','Allura-Regular.otf','Antonio-Bold.ttf','Antonio-Light.ttf','Antonio-Regular.ttf','Arizonia-Regular.ttf','Bebas-Regular.ttf','blackjack.otf','Caviar_Dreams_Bold.ttf','CaviarDreams_BoldItalic.ttf','CaviarDreams_Italic.ttf','CaviarDreams.ttf','Chunk Five Print.otf','ChunkFive-Regular.otf','CooperHewitt-Bold.otf','CooperHewitt-BoldItalic.otf','CooperHewitt-Book.otf','CooperHewitt-BookItalic.otf','CooperHewitt-Heavy.otf','CooperHewitt-HeavyItalic.otf','CooperHewitt-Light.otf','CooperHewitt-LightItalic.otf','CooperHewitt-Medium.otf','CooperHewitt-MediumItalic.otf','CooperHewitt-Semibold.otf','CooperHewitt-SemiboldItalic.otf','CooperHewitt-Thin.otf','CooperHewitt-ThinItalic.otf','DancingScript-Regular.otf','FFF_Tusj.ttf','FiraSans-Bold.otf','FiraSans-BoldItalic.otf','FiraSans-Book.otf','FiraSans-BookItalic.otf','FiraSans-Eight.otf','FiraSans-EightItalic.otf','FiraSans-ExtraBold.otf','FiraSans-ExtraBoldItalic.otf','FiraSans-ExtraLight.otf','FiraSans-ExtraLightItalic.otf','FiraSans-Four.otf','FiraSans-FourItalic.otf','FiraSans-Hair.otf','FiraSans-HairItalic.otf','FiraSans-Heavy.otf','FiraSans-HeavyItalic.otf','FiraSans-Italic.otf','FiraSans-Light.otf','FiraSans-LightItalic.otf','FiraSans-Medium.otf','FiraSans-MediumItalic.otf','FiraSans-Regular.otf','FiraSans-SemiBold.otf','FiraSans-SemiBoldItalic.otf','FiraSans-Thin.otf','FiraSans-ThinItalic.otf','FiraSans-Two.otf','FiraSans-TwoItalic.otf','FiraSans-Ultra.otf','FiraSans-UltraItalic.otf','FiraSans-UltraLight.otf','FiraSans-UltraLightItalic.otf','GrandHotel-Regular.otf','GreatVibes-Regular.otf','JosefinSans-Bold.ttf','JosefinSans-BoldItalic.ttf','JosefinSans-Italic.ttf','JosefinSans-Light.ttf','JosefinSans-LightItalic.ttf','JosefinSans-Regular.ttf','JosefinSans-SemiBold.ttf','JosefinSans-SemiBoldItalic.ttf','JosefinSans-Thin.ttf','JosefinSans-ThinItalic.ttf','KaushanScript-Regular.otf','Lato-Black.ttf','Lato-BlackItalic.ttf','Lato-Bold.ttf','Lato-BoldItalic.ttf','Lato-Hairline.ttf','Lato-HairlineItalic.ttf','Lato-Heavy.ttf','Lato-HeavyItalic.ttf','Lato-Italic.ttf','Lato-Light.ttf','Lato-LightItalic.ttf','Lato-Medium.ttf','Lato-MediumItalic.ttf','Lato-Regular.ttf','Lato-Semibold.ttf','Lato-SemiboldItalic.ttf','Lato-Thin.ttf','Lato-ThinItalic.ttf','LeagueGothic-CondensedItalic.otf','LeagueGothic-CondensedRegular.otf','LeagueGothic-Italic.otf','LeagueGothic-Regular.otf','LeagueSpartan-Bold.otf','Lobster_1.3.otf','LobsterTwo-Bold.otf','LobsterTwo-BoldItalic.otf','LobsterTwo-Italic.otf','LobsterTwo-Regular.otf','norwester.otf','OpenSans-Bold.ttf','OpenSans-BoldItalic.ttf','OpenSans-ExtraBold.ttf','OpenSans-ExtraBoldItalic.ttf','OpenSans-Italic.ttf','OpenSans-Light.ttf','OpenSans-LightItalic.ttf','OpenSans-Regular.ttf','OpenSans-Semibold.ttf','OpenSans-SemiboldItalic.ttf','Oswald-Bold.ttf','Oswald-BoldItalic.ttf','Oswald-Demi-BoldItalic.ttf','Oswald-DemiBold.ttf','Oswald-Extra-LightItalic.ttf','Oswald-ExtraLight.ttf','Oswald-Heavy.ttf','Oswald-HeavyItalic.ttf','Oswald-Light.ttf','Oswald-LightItalic.ttf','Oswald-Medium.ttf','Oswald-MediumItalic.ttf','Oswald-Regular.ttf','Oswald-RegularItalic.ttf','Oswald-Stencil.ttf','PlayfairDisplay-Black.otf','PlayfairDisplay-BlackItalic.otf','PlayfairDisplay-Bold.otf','PlayfairDisplay-BoldItalic.otf','PlayfairDisplay-Italic.otf','PlayfairDisplay-Regular.otf','PlayfairDisplaySC-Black.otf','PlayfairDisplaySC-BlackItalic.otf','PlayfairDisplaySC-Bold.otf','PlayfairDisplaySC-BoldItalic.otf','PlayfairDisplaySC-Italic.otf','PlayfairDisplaySC-Regular.otf','Poppins-Black.otf','Poppins-BlackItalic.otf','Poppins-Bold.otf','Poppins-BoldItalic.otf','Poppins-ExtraBold.otf','Poppins-ExtraBoldItalic.otf','Poppins-ExtraLight.otf','Poppins-ExtraLightItalic.otf','Poppins-Italic.otf','Poppins-Light.otf','Poppins-LightItalic.otf','Poppins-Medium.otf','Poppins-MediumItalic.otf','Poppins-Regular.otf','Poppins-SemiBold.otf','Poppins-SemiBoldItalic.otf','Poppins-Thin.otf','Poppins-ThinItalic.otf','PTC55F.ttf','PTC75F.ttf','PTN57F.ttf','PTN77F.ttf','PTS55F.ttf','PTS56F.ttf','PTS75F.ttf','PTS76F.ttf','Quicksand_Dash.otf','Quicksand-Bold.otf','Quicksand-BoldItalic.otf','Quicksand-Italic.otf','Quicksand-Light.otf','Quicksand-LightItalic.otf','Quicksand-Regular.otf','Raleway-Black.ttf','Raleway-BlackItalic.ttf','Raleway-Bold.ttf','Raleway-BoldItalic.ttf','Raleway-ExtraBold.ttf','Raleway-ExtraBoldItalic.ttf','Raleway-ExtraLight.ttf','Raleway-ExtraLightItalic.ttf','Raleway-Italic.ttf','Raleway-Light.ttf','Raleway-LightItalic.ttf','Raleway-Medium.ttf','Raleway-MediumItalic.ttf','Raleway-Regular.ttf','Raleway-SemiBold.ttf','Raleway-SemiBoldItalic.ttf','Raleway-Thin.ttf','Raleway-ThinItalic.ttf','RedHatDisplay-Black.otf','RedHatDisplay-BlackItalic.otf','RedHatDisplay-Bold.otf','RedHatDisplay-BoldItalic.otf','RedHatDisplay-Italic.otf','RedHatDisplay-Medium.otf','RedHatDisplay-MediumItalic.otf','RedHatDisplay-Regular.otf','RedHatText-Bold.otf','RedHatText-BoldItalic.otf','RedHatText-Italic.otf','RedHatText-Medium.otf','RedHatText-MediumItalic.otf','RedHatText-Regular.otf','Roboto-Black.ttf','Roboto-BlackItalic.ttf','Roboto-Bold.ttf','Roboto-BoldItalic.ttf','Roboto-Italic.ttf','Roboto-Light.ttf','Roboto-LightItalic.ttf','Roboto-Medium.ttf','Roboto-MediumItalic.ttf','Roboto-Regular.ttf','Roboto-Thin.ttf','Roboto-ThinItalic.ttf','RobotoCondensed-Bold.ttf','RobotoCondensed-BoldItalic.ttf','RobotoCondensed-Italic.ttf','RobotoCondensed-Light.ttf','RobotoCondensed-LightItalic.ttf','RobotoCondensed-Regular.ttf','Sofia-Regular.otf','Titillium-Black.otf','Titillium-Bold.otf','Titillium-BoldItalic.otf','Titillium-BoldUpright.otf','Titillium-Light.otf','Titillium-LightItalic.otf','Titillium-LightUpright.otf','Titillium-Regular.otf','Titillium-RegularItalic.otf','Titillium-RegularUpright.otf','Titillium-Semibold.otf','Titillium-SemiboldItalic.otf','Titillium-SemiboldUpright.otf','Titillium-Thin.otf','Titillium-ThinItalic.otf','Titillium-ThinUpright.otf']

def gen_data(word):
    for i in range(0,len(font_list)):
        if __name__ == '__main__':
            fontname = 'Fonts/{}'.format(font_list[i])
            fontsize = 60 
            text = word
            colorText = "black"
            colorOutline = "white"
            colorBackground = "white"
            font = ImageFont.truetype(fontname, fontsize)
            width, height = getSize(text, font)
            img = Image.new('RGB', (width, height), colorBackground)
            d = ImageDraw.Draw(img)
            d.text((width/height, height/30), text, fill=colorText, font=font)
            d.rectangle((0, 0, width*width*len(text), height*5), outline=colorOutline)
            img.save("Images/image{}.png".format(i))
        if __name__ == '__main__':
            fontname = 'Fonts/{}'.format(font_list[i])
            fontsize = 60 
            text = word
            colorOutline = "black"
            colorText = "white"
            colorBackground = "black"
            font = ImageFont.truetype(fontname, fontsize)
            width, height = getSize(text, font)
            img = Image.new('RGB', (width, height), colorBackground)
            d = ImageDraw.Draw(img)
            d.text((width/height, height/30), text, fill=colorText, font=font)
            d.rectangle((0, 0, width*width*len(text), height*5), outline=colorOutline)
            img.save("Images/image_inverse_{}.png".format(i))

def gen_rotated_data(word):
    for i in range(0,len(font_list)):
        if __name__ == '__main__':
            fontname = 'Fonts/{}'.format(font_list[i])
            fontsize = 60 
            text = word
            colorText = "black"
            colorOutline = "white"
            colorBackground = "white"
            font = ImageFont.truetype(fontname, fontsize)
            width, height = getSize(text, font)
            img = Image.new('RGB', (width, height), colorBackground)
            d = ImageDraw.Draw(img)
            d.text((width/height, height/30), text, fill=colorText, font=font)
            d.rectangle((0, 0, width*width*len(text), height*5), outline=colorOutline)
            rotated_image = img.rotate(180)
            rotated_image.save("Rotated Images/image{}.png".format(i))
        if __name__ == '__main__':
            fontname = 'Fonts/{}'.format(font_list[i])
            fontsize = 60 
            text = word
            colorOutline = "black"
            colorText = "white"
            colorBackground = "black"
            font = ImageFont.truetype(fontname, fontsize)
            width, height = getSize(text, font)
            img = Image.new('RGB', (width, height), colorBackground)
            d = ImageDraw.Draw(img)
            d.text((width/height, height/30), text, fill=colorText, font=font)
            d.rectangle((0, 0, width*width*len(text), height*5), outline=colorOutline)
            rotated_image = img.rotate(180)
            rotated_image.save("Rotated Images/image_inverse_{}.png".format(i))

def gen_ambigram_training(image_1,image_2):
    gen_data(image_1)
    gen_rotated_data(image_2)

