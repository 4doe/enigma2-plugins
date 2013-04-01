#!/bin/sh
# AutoBouquets E2 28.2E by LraiZer for www.ukcvs.org

versiondate="1st March 2013"
start_time=`date +%s`
date

rm -f /tmp/*.tv
rm -f /tmp/*.radio
rm -f /tmp/sdt*.txt
rm -f /tmp/bat*.txt

if [ ! "$2" = "" ]; then
	data=`printf "%04x\n" "$1"`
	DATA1="$(expr substr $data 1 2) $(expr substr $data 3 2)"
	REGION1="$2"
else
	DATA1="10 05"
	REGION1="01"
fi

if [ ! "$REGION1" = "21" -a ! "$REGION1" = "32" ]; then
	DATA2="10 08"
	REGION2="21"
else
	DATA2="10 05"
	REGION2="01"
fi

if [ "$3" = "Y" ]; then
	HDFIRST="true"
else
	HDFIRST="false"
fi

#write official numbers?
if [ "$4" = "N" ]; then
	NUMBERING="false"
else
	NUMBERING="true"
fi

#internal/service scan?
if [ "$5" = "N" ]; then
	UPDATE="false"
else
	UPDATE="true"
fi

#placeholder type?
if [ "$6" = "Y" ]; then
	#Pli based image type
	PLACEHOLDER_FLAG="true"
else
	#standard image type
	PLACEHOLDER_FLAG="false"
fi

#parental control for adult, gaming and dating?
if [ "$7" = "Y" ]; then
	PARENTAL_CONTROL="true"
else
	PARENTAL_CONTROL="false"
fi

#force default bouquets?
if [ "$8" = "N" ]; then
	DEFAULT_BOUQUETS="false"
else
	DEFAULT_BOUQUETS="true"
fi

#custom channel ordering?
if [ "$9" = "Y" ]; then
	CUSTOM="true"
else
	CUSTOM="false"
fi

#create fta only?
if [ "$10" = "Y" ]; then
	FTA_ONLY="true"
else
	FTA_ONLY="false"
fi

if [ "$11" = "N" ]; then
	SCRIPTCHECKS="false"
else
	SCRIPTCHECKS="true"
fi

#set bouquet style?
STYLE="$12"
case "$STYLE" in
	"2") STY="";;
	"3") STY="";;
	"4") STY=" = =  ";;
	"5") STY="";;
	  *) STY=" - -  ";;
esac
	
# Autobouquets E2 (default)
if [ "$1" = "None" ]; then
	DATA1="10 05"
	REGION1="01"
	DATA2="10 08"
	REGION2="21"
	HDFIRST="false"
	NUMBERING="true"
	UPDATE="true"
	PLACEHOLDER_FLAG="false"
	PARENTAL_CONTROL="false"
	DEFAULT_BOUQUETS="true"
	CUSTOM="false"
	FTA_ONLY="false"
	SCRIPTCHECKS="true"
	STYLE="0"; STY="  - -  "
fi

read_sdt(){
	s1='^Transport_Stream_ID:'
	s2='^    Service_id:'
	s3='^    Free_CA_mode:'
	s4='^            service_provider_name:'
	s5='^            Service_name:'
	dvbsnoop -s sec -tn -timeout 3000 -ph 2 -f 0x42 -m 0xFF -n 5 0x11 |\
	sed -n '/\('"$s1\|$s2\|$s3\|$s4\|$s5"'\)/p;/DVB-DescriptorTag: 192 /,/ \{15\}/p'|\
	sed 's/^ \{15\}/NVOD_name: /;s/^[ \t]*//' > /tmp/sdt.txt
	dvbsnoop -s sec -tn -timeout 3000 -ph 2 -f 0x46 -m 0xFF -n 500 0x11 |\
	sed -n '/\('"$s1\|$s2\|$s3\|$s4\|$s5"'\)/p;/DVB-DescriptorTag: 192 /,/ \{15\}/p'|\
	sed 's/^ \{15\}/NVOD_name: /;s/^[ \t]*//' >> /tmp/sdt.txt
}

read_bat(){
	bat1="^4a.......$DATA1"
	bat2="^4a.......$DATA2"
	dvbsnoop -s sec -tn -timeout 3000 -ph 2 -pd 0 -f 0x4a -m 0xFF -n 500 0x11 |\
	sed -n '/\('"$bat1\|$bat2"'\)/p' > /tmp/bat_unsorted.txt
	sed -n '/'"$bat1"'/p' /tmp/bat_unsorted.txt | sort -u | sed 's/ //g' >/tmp/bat1.txt
	sed -n '/'"$bat2"'/p' /tmp/bat_unsorted.txt | sort -u | sed 's/ //g' >/tmp/bat2.txt
	rm -f /tmp/bat_unsorted.txt
}

read_nit(){
	n1='^    Transport_stream_ID:'
	n2='^            Frequency:'
	n3='^            Polarisation:'
	n4='^            Kind:'
	n5='^            Roll Off Faktor:'
	n6='^            Modulation_type:'
	n7='^            Symbol_rate:'
	n8='^            FEC_inner:'
	dvbsnoop -n 5 -nph 0x10 |\
	sed -n '/\('"$n1\|$n2\|$n3\|$n4\|$n5\|$n6\|$n7\|$n8"'\)/p'|\
	sed 's/^[ \t]*//' >/tmp/nit.txt
}

check_update(){
	if [ -e /etc/enigma2/bouquets.$1 ]; then
		if [ "$DEFAULT_BOUQUETS" = "true" ] || ! grep -q 'userbouquet.ukcvs' /etc/enigma2/bouquets.$1 >/dev/null 2>&1; then
			sed -i '$d' /tmp/bouquets.$1
			cat /etc/enigma2/bouquets.$1 | sed '/userbouquet.ukcvs/d' | sed '1d' >>/tmp/bouquets.$1
		else
			rm -f /tmp/bouquets.$1
		fi
	fi
}

fwget(){
	wget -q -O - http://127.0.0.1/web/$1
}

create_lamedb(){
echo 'eDVB services /4/
transponders
011a0000:07dc:0002
	s 11934000:27500000:1:2:282:2:0
/
end
services
1199:011a0000:07dc:0002:1:0
Sky
p:BSkyB
end
Created by AutoBouquets E2' >/etc/enigma2/lamedb
}

init_lamedb(){
sed -i '/^transponders/c\
transponders\
011a0000:07dc:0002\
	s 11934000:27500000:1:2:282:2:0\
/
/^services/c\
services\
1199:011a0000:07dc:0002:1:0\
Sky\
p:BSkyB' /etc/enigma2/lamedb
}

if [ "$SCRIPTCHECKS" = "true" ]; then
	if [ ! -e /usr/bin/dvbsnoop ]; then
		echo "dvbsnoop not found!"
		exit 0
	fi
	
	#wake from standby?
	if fwget "powerstate"|grep -q 'instandby>true' >/dev/null 2>&1; then
		echo "autobouquets script is waking up from standby, wait..."
		fwget "powerstate?newstate=4" >/dev/null 2>&1
		scriptfromstandby="true"
		sleep 10
	fi

	#set channel 999 as the default fallback service
	defaultservice="1:0:2:1199:7dc:2:11a0000:0:0:0:"

	init="false"
	#check if we need to initialize system with default service?
	if [ ! -e /etc/enigma2/lamedb ]; then
		init="true"
		create_lamedb
	else
		#check if we have default transponder for default service?
		if ! `grep -q '^011a0000:07dc:0002' /etc/enigma2/lamedb`; then
			init="true"
			init_lamedb
		fi
	fi
	if [ "$init" = "true" ]; then
		echo "AutoBouquets is initializing your system, please wait..."
		fwget "servicelistreload?mode=1" >/dev/null 2>&1
		fwget "zap?sRef=$defaultservice" >/dev/null 2>&1
		sleep 60
	fi 

	#get pre scan service for zap back
	prescanservice=`fwget "subservices"|grep 'servicereference'|sed 's/.*>\(.*\)<.*$/\1/'`

	#check pre scan service is a vaild 28.2E service?
	if [ ! `echo "$prescanservice"|cut -d ":" -f6` = "2" ]; then
		[ "$prescanservice" = "N/A" -o "$prescanservice" = "" ] && prescanservice="$defaultservice"
		echo "autobouquets script is zapping to default valid service, wait..."
		fwget "zap?sRef=$defaultservice" >/dev/null 2>&1
		sleep 60
	fi

	#check we are now on a valid 28.2E service
	if ! fwget "about"|grep -q 'onid>2<'; then
		echo "please zap to an ACTIVE 28.2E channel"
		exit 0
	fi
fi

echo "
Settings:
[1] Data is $DATA1, Region is $REGION1
[2] Data is $DATA2, Region is $REGION2
HD First is $HDFIRST, Numbered is $NUMBERING
Updated is $UPDATE, Placeholder is $PLACEHOLDER_FLAG
Parental is $PARENTAL_CONTROL, Default is $DEFAULT_BOUQUETS
Custom is $CUSTOM, FTA Only is $FTA_ONLY
"

echo "reading Service Description Table"
read_sdt

echo "reading Bouquet Association Table"
read_bat

echo "parsing Service Description Table"
echo "parsing Bouquet Association Table $REGION1"
echo "parsing Bouquet Association Table $REGION2"
echo "merging Bouquet Association Table"
echo -e "merging BAT Tables and SDT Tables\n"

cd /usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/
./autobouquets "00$REGION1" "00$REGION2" "$HDFIRST" "$NUMBERING" "$UPDATE" "$PLACEHOLDER_FLAG" "$PARENTAL_CONTROL" "$CUSTOM" "$FTA_ONLY" "$STYLE"

echo -e "writing Bouquets and Services\n"

check_update "tv"
check_update "radio"

if [ "$UPDATE" = "true" ]; then
	#scan Network Information Table for current transponder list
	#update lamedb with services from BAT, transponders from NIT
	
	echo "reading Network Information Table"
	read_nit

	echo -e "process NIT transponders services\n"
	cd /usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/
	./autolamedb
	
	echo "Updating Services"

	end=`grep -n '^end' /etc/enigma2/lamedb | sed 'q' | cut -d ":" -f1`
	sed -n "1,$end{p}" /etc/enigma2/lamedb | sed '$d' |\
	sed '/^.*:.*:0002$/,/\//d' >/tmp/lamedb_transponders.txt
	cat /tmp/nit_sorted.txt >>/tmp/lamedb_transponders.txt
	echo "end" >>/tmp/lamedb_transponders.txt
	rm -f /tmp/nit_sorted.txt

	sed -n "/^services/,/^end/p" /etc/enigma2/lamedb | sed '$d' |\
	sed '/.*:.*:.*:0002:.*/,/^p:/d' >/tmp/lamedb_strip.txt
	cat /tmp/lamedb_transponders.txt /tmp/lamedb_strip.txt /tmp/lamedb_services.txt >/tmp/lamedb
	echo "end" >>/tmp/lamedb
	echo "Updated by AutoBouquets on `date`" >>/tmp/lamedb

	rm -f /tmp/lamedb_transponders.txt
	rm -f /tmp/lamedb_services.txt
	rm -f /tmp/lamedb_strip.txt
	mv /tmp/lamedb /etc/enigma2/
fi

#write autobouquets info to last bouquet
SD='#SERVICE 1:0:1:2331:7ee:2:11a0000:0:0:0:
#DESCRIPTION'
echo "#NAME $STY AutoBouquets
#SERVICE 1:64:1:0:0:0:0:0:0:0:
#DESCRIPTION 28.2E -- About --
$SD  
$SD Plugin Version date - $versiondate
$SD Created on `date`
$SD  
$SD Created by AutoBouquets E2
$SD binary code, python coding
$SD frontend scripts by LraiZer
$SD Developed by www.ukcvs.org
$SD  
$SD GUI, python coding - AndyBlac
$SD  
$SD Thanks to ViX TEAM members
$SD for feedback and beta testing
$SD www.world-of-satellite.com" >/tmp/userbouquet.ukcvs16.tv

mv /tmp/*.tv /etc/enigma2/
mv /tmp/*.radio /etc/enigma2/

echo -e "Updating Bouquets\n"
if [ "$UPDATE" = "true" ]; then
	reload=0
else
	reload=2
fi
wget -q -O - http://127.0.0.1/web/servicelistreload?mode=$reload >/dev/null

date
stop_time=$(expr `date +%s` - $start_time)
log_time="Process Time: "$(expr $stop_time / 60)" minutes "$(expr $stop_time % 60)" seconds"
echo -e "$log_time\n"
echo "$log_time" >>/tmp/autobouquets.log
date >>/tmp/autobouquets.log
mv /tmp/autobouquets.log /usr/lib/enigma2/python/Plugins/Extensions/AutoBouquets/

if [ "$SCRIPTCHECKS" = "true" ]; then
	#zap back to valid pre scan service?
	if [ ! "$(fwget "subservices"|grep 'servicereference'|sed 's/.*>\(.*\)<.*$/\1/')" = "$prescanservice" ]; then
		fwget "zap?sRef=$prescanservice" >/dev/null 2>&1
		echo "autobouquets script is Zapping back, wait..."
		sleep 60
	fi
	
	#sleep to standby?
	if [ "$scriptfromstandby" = "true" ]; then
		fwget "powerstate?newstate=5" >/dev/null 2>&1
		echo "autobouquets script is going to sleep in standby!"
	fi
fi

exit 0
