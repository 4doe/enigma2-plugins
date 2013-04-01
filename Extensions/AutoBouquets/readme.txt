------------------------------------------------
AutoBouquets E2 for satellite 28.2E 
Version date - 1st March 2013
Created by LraiZer - www.ukcvs.org
------------------------------------------------

Plugin Usage
----------------
first perform a scan on 28.2e satellite so that you
have the latest lamedb service file for 28.2 East.

next zap to an active channel on 28.2e so that we can
get dvbsnoop to read the bouquet data from the stream.

now its time to select AutoBouquets E2 Plugin from the
plugins menu and choose your nearest localized region.

generated bouquets are prepended to any existing
bouquets so your current bouquets are not overwritten.

sit back and watch for a few minutes as your regional
bouquets are read and generated direct from the stream.

Menus
----------------
 - Local Area Selection
 generate selected bouquets for your SD/HD local region.
 
 - Use HD First Bouquet
 puts the HD channels starting at position 6 immediately
 after 1-5 (BBC1, BBC2, ITV1, C4, C5 for your region).
 yes = placeholder channels are put in category bouquets.
 no = placeholder channels are put in first bouquet only.
 
 - Show Channel Numbers
 puts epg position number in front of the channel names.
 
 - Use Internal NIT Scan
 updates the lamedb with latest transponders and services
 by scanning Network Information Table via script instead
 of running standard 28.2e engima2 automatic service scan.
  
 - Use Pli Placeholders
 yes = allows placeholder skipping on openpli based images.
 allows placeholder hiding if supported by engima2 version.
 no = uses normal services for placeholder channels as none
 pli based images do not assign correct positions using pli. 
 
 - Create Child Friendly
 dont generate the adult or the gaming and dating bouquets.
 
 - Make Default Bouquets
 this will force default bouquet categories to be generated.
 if you wish to remove any bouquets from future generations,
 delete the bouquets you dont want and disable this option.

 - Custom Channel Order
 this allows you to change the generated channel ordering.
 edit the example custom.txt file in /AutoBouquets/ folder
 by changing the second channel number 101-999 accordingly. 
  
 - Scan Free To Air Only
 this will generate services with free to air flag detection.
  
 - Scheduled Update Scan
 this allows you to set a daily, weekly, monthly update timer.

Tips
----------------
if you want 1, 2, 3 button presses for BBC1, BBC2, ITV1.
simply remove your "28.2E ---- UK Bouquets ---" bouquet.
this will remove the official epg numbering and set your
Entertainment bouquet channels to starting with 1, 2, 3.

the Plugin does not re-create any bouquets that have been
previously removed by the user. if for example you remove
the adult bouquet, it will remain removed the next time
you run the plugin and so remain child friendly updatable.
you will need to turn the default bouquets option to "off"
you can set default option to create first bouquets again.

changing the order of the bouquets also remains static and
does not get re-ordered on subsequent runs. this will have
to be done while not using the HD Bouquet settings option,
or your offical numbering with not be correct and match up.

when creating a custom.txt file for personal channel order,
enter the two channel you wish to switch with each other.

101=143
103=178
104=230
105=171

when using the supplement.txt file to manually add channels,
its best to add your channel with a channel number that puts
the new channel into an empty slot in the "other" bouquet.
current empty slots are 975 < 995. you can then simply add a
switch entry in the custom.txt file to swap with another one.

Prerequisites
----------------
dvbsnoop binary is required in /usr/bin/ folder.
frontend GUI should work on systems using Enigma2,
backend script should work on most linux systems.

script requires all the common busybox functions:
grep, sed, cat, printf, wget, echo, mv, rm, date.
plus busybox math support for arithmetic $((1+1))
all these should be standard in your linux image.


Manual Installation - AutoBouquets_E2.rar (archive)
---------------
1) make sure you have dvbsnoop in your /usr/bin/

2) place files onto engima2 box in relevant folders.
   make autobouquets_e2.sh executable (chmod 755)

3) restart Enigma2 to reload AutoBouquets E2 plugin

HOW TO: install required dvbsnoop on openpli image?
telnet to your box and type the following command:

opkg update && opkg install dvbsnoop 


Version infos
---------------
10-08-2012
 first version released to public for testing, this
 is totaly untested, so backup your files first! :)

13-08-2012
 current bouquets are no longer overwritten. if not
 detected as already present in user bouquets, they
 are written to front to preserve official numbering.
 various other code fixes and imporvements also done.

19-08-2012
 new GUI with help button for onbox readme.txt viewing.
 error checks added to stop box lockup on none active.
 added special handling of the sbo channels namespace.
 other file and error checking and various code fixes.

21-08-2012
 added checks to make sure we only process 28.2E sat.
 also .ipk installer for mipsel with dvbsnoop depend.

24-09-2012
 LraiZer:-
 auto update lamedb services using script NIT scanning.
 option to parentally control and make child friendly.
 option to add official channel numbering with names.
 option to use channel placeholder on none PLi images.
 option to be able to create the default bouquet set.
 option to be able to create free to air only bouquets.
 option to create customized channel ordered bouquets, 
 use example custom.txt in plugin folder to customize.

 AndyBlac:- OE-Alliance: https://github.com/oe-alliance/
            oe-alliance-plugins/tree/master/AutoBouquets
 new GUI, which will now remember and save your settings.
 option to keep official numbering with HD first bouquet.
 auto schedule for Daily, Weekly, Monthly at chosen time.
 perform a service scan before running script (optional).
 compatible with PLi based image placeholder skipping.
 compatible with iDreamX Bouquet Editor for Apple MAC.
 Thanks to ViX TEAM members for feedback and beta testing.

27-09-2012
 auto detect correct transponder modulation with NIT scan.
 adds full list of active channels to interactive bouquet.
 removed needsRestart paramater, feedback crashes on some.

30-09-2012
 fix unassigned option crash in scheduled service scanning.
 remove duplicated channel epg numbering list in custom.txt

9-10-2012
 now also detects and parses the hidden data channel names.
 add autobouquets selection menu to service searching menu.
 also adds the channel epg numbers to the official bouquet.

13-10-2012
 now also auto initializes systems for first run of plugin.

21-02-2013
 AutoBouquets E2 code has been 90% rewritten and optimized
 for speed. main coding has now been moved into binaries.
 script checking can be disabled for none comaptible boxes.
 run AutoBouquets Downloader in background via blue button.
 custom.txt channel swap file has be slightly simplified.
 now just enter channels to swap with each other. 105=171

01-03-2013
 fixed missing channels bug. added bouquet style options. 
 added supplement.txt file for manual service additions.

------------------------------------------------------
  www.ukcvs.org thanks you for using AutoBouquets E2
  thanks to PaphosAL for plugin icon.   HAVE FUN!
------------------------------------------------------
