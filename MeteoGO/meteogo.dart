import 'dart:convert';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:intl/intl.dart';
import 'package:http/http.dart' as http;
import 'package:geolocator/geolocator.dart';
import 'package:geocoder/geocoder.dart';
import '../util/weather_util.dart';
import '../models/forecast_model.dart';
import '../network/network.dart';
import '../ui/enable_gps.dart';

class ForecastGroup extends StatefulWidget {

  @override
  _ForecastGroupState createState() => _ForecastGroupState();
}

class _ForecastGroupState extends State<ForecastGroup> {


  Future<ForecastModel> forecastObject;

  final myTxtController = TextEditingController();

  String _cityName;

  Position position;

  int hour;
  int hourIndex = 0;
  int day;
  int dayIndex = 0;

  List dotw = const ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];

  var cityName;
  var cityCountry;
  var cityLat;
  var cityLon;

  void _incrementHour() {
    setState(() {
      if (hourIndex < 47) {
        if (hour == 23) {
          day = (day + 1) % 7;
          dayIndex++;
        }
        hour = (hour + 1) % 24;
        hourIndex++;
      }
    });
  }

  void _decrementHour() {
    setState(() {
      if (hourIndex > 0) {
        if (hour == 0) {
          day = (day - 1) % 7;
          dayIndex--;
        }
        hour = (hour - 1) % 24;
        hourIndex--;
      }
    });
  }

  void _setCurrentHourDay() {
    DateTime now = DateTime.now();
    hour = int.parse(DateFormat('H').format(now));
    day = dotw.indexOf(DateFormat('EEE').format(now).toUpperCase()); //'TUE'
  }

  void _incrementDay() {
    setState(() {
      if (dayIndex < 2) {
        day = (day + 1) % 7;
        dayIndex++;
        if (hourIndex > 23) {
          int hourDif = hourIndex;
          hourIndex = 47;
          hour = (hour + (hourIndex - hourDif)) % 24;
        } else {
          hourIndex += 24;
        }
      }
    });
  }

  void _decrementDay() {
    setState(() {
      if (dayIndex > 0) {
        day = (day - 1) % 7;
        dayIndex--;
        if (hourIndex < 24) {
          int hourDif = hourIndex;
          hourIndex = 0;
          hour = (hour - hourDif) % 24;
        } else {
          hourIndex -= 24;
        }
      }
    });
  }

  Widget weatherIcon(int id) {
    int sun = 800;
    int clouds_sun = 801;
    List clouds_sun_rain_1 = [500, 501];
    List clouds_sun_rain_2 = [502, 503, 504];
    int clouds = 802;
    List clouds_2 = [803, 804];
    List clouds_2_rain_1 = [300, 301];
    List clouds_2_rain_2 = [302, 310, 311, 312, 313, 314, 321, 520, 521, 522, 531];
    List clouds_2_bolt = [210, 211, 212, 221];
    List clouds_2_bolt_rain_1 = [200, 201, 230, 231];
    List clouds_2_bolt_rain_2 = [202, 232];
    List snow = [511, 600, 601, 602, 611, 612, 613, 615, 616, 620, 621, 622];
    List mist = [701, 711, 721, 731, 741, 751, 761, 762, 771, 781];

    if (id == sun) {
      return Image.asset('assets/icons/sun.png');
    }
    if (id == clouds_sun) {
      return Image.asset('assets/icons/clouds_sun.png');
    }
    if (clouds_sun_rain_1.contains(id)) {
      return Image.asset('assets/icons/clouds_sun_rain_1.png');
    } else if (clouds_sun_rain_2.contains(id)) {
      return Image.asset('assets/icons/clouds_sun_rain_2.png');
    } else if (id == clouds) {
      return Image.asset('assets/icons/clouds.png');
    } else if (clouds_2.contains(id)) {
      return Image.asset('assets/icons/clouds_2.png');
    } else if (clouds_2_rain_1.contains(id)) {
      return Image.asset('assets/icons/clouds_2_rain_1.png');
    } else if (clouds_2_rain_2.contains(id)) {
      return Image.asset('assets/icons/clouds_2_rain_2.png');
    } else if (clouds_2_bolt.contains(id)) {
      return Image.asset('assets/icons/clouds_2_bolt.png');
    } else if (clouds_2_bolt_rain_1.contains(id)) {
      return Image.asset('assets/icons/clouds_2_bolt_rain_1.png');
    } else if (clouds_2_bolt_rain_2.contains(id)) {
      return Image.asset('assets/icons/clouds_2_bolt_rain_2.png');
    } else if (snow.contains(id)) {
      return Image.asset('assets/icons/snow.png');
    } else if (mist.contains(id)) {
      return Image.asset('assets/icons/mist.png');
    } else {
      return Image.asset('assets/icons/404.png');
    }
  }

  Future getWeather() async {
    http.Response response = await http.get(
      'http://api.openweathermap.org/data/2.5/weather?q=' +
        _cityName +
        '&units=metric&appid=' +
        Util.weatherAPI);
    var results = jsonDecode(response.body);

    if (response.statusCode == 200) {
      setState(() {
      this.cityName = results['name'];
      this.cityCountry = results['sys']['country'];
      this.cityLat = results['coord']['lat'];
      this.cityLon = results['coord']['lon'];
      }); 
    } else {
      AlertDialog(content: Text(':('));
    }
  }

  Future<ForecastModel> getForecast() async {
    await getWeather();
    var finalUrl = 'https://api.openweathermap.org/data/2.5/onecall?lat=' +
        cityLat.toString() +
        '&lon=' +
        cityLon.toString() +
        '&exclude=minutely,alerts&units=metric&appid=' +
        Util.weatherAPI;

    final response = await http.get(Uri.encodeFull(finalUrl));

    if (response.statusCode == 200) {
      print('Forecast data: ${response.body}');
      return ForecastModel.fromJson(json.decode(response.body));
    } else {
      throw Exception('Error getting forecast data');
    }
  }

  Future getCurrentLocation() async{
    position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);

    var coordinates = new Coordinates(position.latitude, position.longitude);
    var addresses = await Geocoder.local.findAddressesFromCoordinates(coordinates);
    var first = addresses.first;
  
    myTxtController.text = '${first.locality}';
  }

  Future updateCurrentLocation() async{
    position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
    var coordinates = new Coordinates(position.latitude, position.longitude);
    var addresses = await Geocoder.local.findAddressesFromCoordinates(coordinates);
    var first = addresses.first;
    _cityName = first.locality;
    cityLat = position.latitude;
    cityLon = position.longitude;
  }

  Future startGetForecast() async{
    setState(() {
      forecastObject = Network().getForecast(lat: position.latitude, lon: position.longitude);
      cityLat = position.latitude;
      cityLon = position.longitude;
    });
  }

  Future updateForecast() async {
    setState(() {
      forecastObject = Network().getForecast(lat: cityLat, lon: cityLon);
      _setCurrentHourDay();
      hourIndex = 0;
      dayIndex = 0;
    });
  }

  @override
  void initState() {
    super.initState();
    SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
    getCurrentLocation().then((value) {
      Future.delayed(Duration.zero);
      startGetForecast();
      loading = false;
    });
    _setCurrentHourDay();
  }
  
  bool loading = true;

  @override
  Widget build(BuildContext context) {
    return loading ? enableGps() :
      FutureBuilder<ForecastModel>(
        future: forecastObject,
        builder: (BuildContext context, AsyncSnapshot<ForecastModel> snapshot) {
          switch (snapshot.connectionState) {
            case ConnectionState.waiting:
              return Center(child: SizedBox(width: 50, height: 50, child: CircularProgressIndicator()));
            default:
              if (snapshot.hasError) {
                print(snapshot.error.toString());
                return Center(
                  child: Text('404 :(',
                      style: TextStyle(
                          height: 1,
                          fontSize: 100.0,
                          color: Colors.white)),
                );
              }
              return Column(
                children: <Widget>[
                  Spacer(flex: 2,),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        width: 50,
                        child: IconButton(
                          icon: Icon(Icons.gps_fixed, color: Colors.white),
                          onPressed: (() {
                            setState(() {
                              updateCurrentLocation().then((_) {
                                getWeather().then((_) {
                                forecastObject = getForecast();
                                myTxtController.text = '$cityName, $cityCountry';
                              });
                              });
                            });
                          })
                        ),
                      ),
                      Expanded(
                        child: TextField(
                          controller: myTxtController,
                          onSubmitted: ((value) {
                            setState(() async{
                              _cityName = value;
                              getWeather().then((_) {
                                forecastObject = getForecast();
                                myTxtController.text = '$cityName, $cityCountry';
                              });
                            });
                          }),
                          decoration: InputDecoration(
                            hintText: 'Search city',
                            border: InputBorder.none,
                            hintStyle: TextStyle(
                              fontWeight: FontWeight.normal,
                              color: Colors.grey[700],
                              fontSize: 25,
                            ),
                          ),
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                            fontSize: 25,
                          ),
                        ),
                      ),
                      Container(
                        width: 50,
                        child: IconButton(
                          icon: Icon(Icons.update, color: Colors.white),
                          onPressed: updateForecast,
                        ),
                      )
                    ],
                  ),
                  Spacer(flex: 4),
                  Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Container(
                            width: 80,
                            child: Text(
                              '${snapshot.data.daily[dayIndex].temp.min.round()}',
                              textAlign: TextAlign.left,
                              style: TextStyle(
                                  fontSize: 50.0, color: Colors.grey[700]),
                            ),
                          ),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Container(
                                  child: Text(
                                      '${snapshot.data.hourly[hourIndex].temp.round()}',
                                      style: TextStyle(
                                          height: 1,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 100.0,
                                          color: Colors.white))),
                              Column(
                                mainAxisAlignment: MainAxisAlignment.end,
                                children: [
                                  Container(
                                    width: 20,
                                    height: 20,
                                    decoration: BoxDecoration(
                                      color: Colors.transparent,
                                      border: Border.all(
                                          color: Colors.white, width: 4),
                                      borderRadius: BorderRadius.circular(10)
                                    )
                                  ),
                            ],
                          ),
                            ],
                          ),
                          Container(
                            width: 80,
                            child: Text(
                              '${snapshot.data.daily[dayIndex].temp.max.round()}',
                              textAlign: TextAlign.right,
                              style: TextStyle(
                                  fontSize: 50.0, color: Colors.grey[700]),
                            ),
                          ),
                        ],
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Spacer(flex: 4),
                          Row(
                            children: [
                              SvgPicture.asset('assets/icons/rain.svg',
                                  color: Colors.white),
                              Text(
                                  ' ${(100 * snapshot.data.hourly[hourIndex].pop).round()}%',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  )),
                            ],
                          ),
                          Spacer(flex: 1),
                          Row(
                            children: [
                              SvgPicture.asset('assets/icons/wind.svg',
                                  color: Colors.white),
                              Text(
                                  ' ${snapshot.data.hourly[hourIndex].windSpeed.round()} m/s',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                  )),
                            ],
                          ),
                          Spacer(flex: 4),
                        ],
                      ),
                    ],
                  ),
                  Spacer(flex: 1),
                  Container(
                    child: weatherIcon(
                        snapshot.data.hourly[hourIndex].weather[0].id),
                    width: 300.0,
                    height: 200.0,
                  ),
                  Spacer(flex: 1),
                  Row(
                    children: [
                      Spacer(flex: 4),
                      IconButton(
                        icon: Icon(Icons.chevron_left, color: dayIndex == 0 ? Colors.grey[700] : Colors.white),
                        iconSize: 50,
                        onPressed: _decrementDay,
                      ),
                      Container(
                        width: 80,
                        height: 50,
                        decoration: BoxDecoration(
                            color: Colors.transparent,
                            border: Border.all(color: Colors.white, width: 2),
                            borderRadius: BorderRadius.circular(25)),
                        child: Center(
                            child: Text('${dotw[day]}',
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold))),
                      ),
                      IconButton(
                        icon: Icon(Icons.chevron_right, color: dayIndex == 2 ? Colors.grey[700] : Colors.white),
                        iconSize: 50,
                        onPressed: _incrementDay,
                      ),
                      Spacer(flex: 4),
                    ],
                  ),
                  Spacer(flex: 1),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      IconButton(
                        icon: Icon(Icons.chevron_left, color: hourIndex == 0 ? Colors.grey[700] : Colors.white),
                        iconSize: 50,
                        onPressed: _decrementHour,
                      ),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.baseline,
                        children: [
                          Center(
                              child: Text('$hour',
                                  style: TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: Colors.white,
                                    fontSize: 60,
                                  ))),
                          Center(
                              child: Text(':00',
                                  style: TextStyle(
                                    color: Colors.grey[700],
                                    fontSize: 40,
                                  ))),
                        ],
                      ),
                      IconButton(
                        icon: Icon(Icons.chevron_right, color: hourIndex == 47 ? Colors.grey[700] : Colors.white),
                        iconSize: 50,
                        onPressed: _incrementHour,
                      ),
                    ],
                  ),
                  Spacer(flex: 2),
                ],
              );
          }
        },
      );
  }
}
