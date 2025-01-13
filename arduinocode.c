<<<<<<< HEAD
#include <DHT.h>

#define DHTPIN 8
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define TRIGPIN 3
#define ECHOPIN 4

#define RED_LED 12
#define GREEN_LED 13

void setup() {
  Serial.begin(9600);
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  dht.begin();
}

void loop() {
  // Measure distance using the ultrasonic sensor
  long duration, distance;
  digitalWrite(TRIGPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);

  duration = pulseIn(ECHOPIN, HIGH);
  distance = duration * 0.034 / 2;

  if (distance <= 50) {
    Serial.println("Object detected within 50 cm.");

    // Read temperature and humidity from the DHT sensor only if object is detected
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
    } else {
      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.print(" °C, Humidity: ");
      Serial.print(humidity);
      Serial.println(" %");

      // Handle RED_LED for high temperatures
      if (temperature > 38) {
        digitalWrite(RED_LED, HIGH);  // Turn on RED_LED if temperature is above 38°C
      } else {
        digitalWrite(RED_LED, LOW);   // Turn off RED_LED if temperature is <= 38°C
      }

      // Handle GREEN_LED behavior
      if (temperature < 38) {
        digitalWrite(GREEN_LED, HIGH);  // Turn on GREEN_LED if temperature is below 38°C
      } else {
        digitalWrite(GREEN_LED, LOW);   // Turn off GREEN_LED if temperature is >= 38°C
      }
    }
  } else {
    Serial.println("No object detected within 50 cm.");

    // Turn off LEDs
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);
  }

  // Check for incoming data from the backend
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();  // Remove any trailing whitespace or newline characters

    if (message == "Mask detected") {
      // Turn on the green light
      digitalWrite(GREEN_LED, HIGH);  // Turn on the green LED
      digitalWrite(RED_LED, LOW);  // Turn off the red LED
    } else if (message == "No mask detected") {
      // Turn on the red light
      digitalWrite(RED_LED, HIGH);  // Turn on the red LED
      digitalWrite(GREEN_LED, LOW);  // Turn off the green LED
    }
  }

  delay(1000);  // Wait for a second before reading again
}
=======
#include <DHT.h>

#define DHTPIN 8
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define TRIGPIN 3
#define ECHOPIN 4

#define RED_LED 12
#define GREEN_LED 13

void setup() {
  Serial.begin(9600);
  pinMode(TRIGPIN, OUTPUT);
  pinMode(ECHOPIN, INPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  dht.begin();
}

void loop() {
  // Measure distance using the ultrasonic sensor
  long duration, distance;
  digitalWrite(TRIGPIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGPIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGPIN, LOW);

  duration = pulseIn(ECHOPIN, HIGH);
  distance = duration * 0.034 / 2;

  if (distance <= 50) {
    Serial.println("Object detected within 50 cm.");

    // Read temperature and humidity from the DHT sensor only if object is detected
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
    } else {
      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.print(" °C, Humidity: ");
      Serial.print(humidity);
      Serial.println(" %");

      // Handle RED_LED for high temperatures
      if (temperature > 38) {
        digitalWrite(RED_LED, HIGH);  // Turn on RED_LED if temperature is above 38°C
      } else {
        digitalWrite(RED_LED, LOW);   // Turn off RED_LED if temperature is <= 38°C
      }

      // Handle GREEN_LED behavior
      if (temperature < 38) {
        digitalWrite(GREEN_LED, HIGH);  // Turn on GREEN_LED if temperature is below 38°C
      } else {
        digitalWrite(GREEN_LED, LOW);   // Turn off GREEN_LED if temperature is >= 38°C
      }
    }
  } else {
    Serial.println("No object detected within 50 cm.");

    // Turn off LEDs
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(RED_LED, LOW);
  }

  // Check for incoming data from the backend
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();  // Remove any trailing whitespace or newline characters

    if (message == "Mask detected") {
      // Turn on the green light
      digitalWrite(GREEN_LED, HIGH);  // Turn on the green LED
      digitalWrite(RED_LED, LOW);  // Turn off the red LED
    } else if (message == "No mask detected") {
      // Turn on the red light
      digitalWrite(RED_LED, HIGH);  // Turn on the red LED
      digitalWrite(GREEN_LED, LOW);  // Turn off the green LED
    }
  }

  delay(1000);  // Wait for a second before reading again
}
>>>>>>> fbbba1c86fe856ae56832b3f9182dbbc5a945594
