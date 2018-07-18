// Libraries
#include <ESP8266WiFi.h>
#include <OneWire.h>
OneWire ds(2);
// WiFi parameters
const char* ssid = "ROBBIE_ROTTEN";
const char* password = "chipster123";

// Host
const char* host = "dweet.io";

void setup() {

  // Start Serial
  Serial.begin(115200);
  delay(10);
  
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void loop() {
  sensors.requestTemperatures(); // Send the command to get temperature readings 
  temp = sensors.getTempCByIndex(0)
  
  Serial.print("Connecting to ");
  Serial.println(host);

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  // This will send the request to the server
  client.print(String("GET /dweet/for/WoodsThermostatOne?temperature=") + temp + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
  Serial.println("pushed data to host t =");
  Serial.print(temp);
  delay(10);
  
  // Read all the lines of the reply from server and print them to Serial
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.println("The following has been read:");
    Serial.print(line);
  }
  
  Serial.println();
  Serial.println("closing connection");

  // Repeat every 10 seconds
  delay(4000);

}
