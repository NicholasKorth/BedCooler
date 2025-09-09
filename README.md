# Bed Cooler Control System

## Overview

This repository contains the hardware design files and STM32 firmware for a dual-zone bed cooling and heating system. The project is designed to provide temperature control for two independent zones of a mattress using Peltier modules (TECs) for thermoelectric cooling and heating.

The system uses a two-processor architecture:
* **Raspberry Pi Compute Module 5 (CM5):** Serves as the high-level application processor. It is intended to run a user interface (UI) on a MIPI DSI touchscreen, allowing users to set target temperatures, create schedules, and manually control all system components.
* **STM32G474 Microcontroller:** Acts as the real-time hardware controller. It receives commands from the CM5 via UART and directly manages the H-bridges, fans, pumps, solenoids, and all sensor readings.

This board is a development platform for creating a responsive sleeping environment.

---
## Hardware Features

### Core Components
* **Microcontroller:** STMicroelectronics **STM32G474RET6**
* **Host Processor:** **Raspberry Pi Compute Module 5 (CM5)**
* **Peltier Drivers:** 2x Texas Instruments **DRV8701ERGER** H-Bridge Gate Drivers, controlling two pairs of TEC-12712 Peltier modules.
* **Audio Amplifier:** Texas Instruments **TAS5805MPWPR** Class-D stereo amplifier with I2S and I2C interfaces, designed for 8-ohm speaker drivers.

### Actuators & Outputs
* **Dual H-Bridges:** For bidirectional (heating/cooling) control of two independent Peltier zones.
* **PWM Fan Control:** Three 4-pin PWM fan headers with tachometer feedback.
* **Pump Drivers:** Two channels for driving 12V water pumps.
* **Solenoid Drivers:** Two channels for controlling 12V solenoid valves.

### Sensors & Inputs
* **Thermistors:** Four dedicated inputs for NTC thermistors to monitor Peltier and water temperatures.
* **Current Sensing:** On-board current sensing circuits for each Peltier H-bridge.
* **Water Presence Sensor:** Input for a water detection sensor.
* **Float Valve Switch:** Input for a reservoir level float switch.
* **H-Bridge Fault Detection:** Dedicated fault inputs from each DRV8701 driver for error handling.

### Connectivity & Peripherals
* **STM32-CM5 Link:** **UART** for command and control.
* **Display:** **MIPI DSI** connector for a touchscreen display.
* **USB Ports:**
    * 1x USB-A 3.0 port.
    * 2x USB-C ports.
* **Video Output:** 1x **HDMI** port.
* **Storage:** On-board **MicroSD card** reader connected to the CM5.

### PCB & Power Specifications
* **Power Input:** Requires a 12V DC power supply capable of providing approximately 350 watts.
* **PCB Layers:** 6-layer board.
* **Design:** Features several impedance-controlled traces for high-speed signals.
* **Stackup:** Designed for JLCpcb stackup JLC06162H-3313.
* **Copper Weight:** 2oz outer copper layers.
* **Via Size:** Minimum via size of 0.2mm hole / 0.35mm diameter.

---
## System Architecture

The division of labor between the two processors is central to the system's design:

* **Raspberry Pi CM5:**
    * Hosts the Linux OS and the user-facing application.
    * Manages the graphical user interface (GUI) on the touchscreen.
    * Handles logic like temperature scheduling, user profiles, and system settings.
    * Sends high-level commands (e.g., "set temperature of zone 1 to 22°C") to the STM32 via UART.
* **STM32G474:**
    * Runs bare-metal or RTOS firmware dedicated to real-time hardware control.
    * Parses commands received from the CM5.
    * Executes the temperature control loop using a hysteresis algorithm.
    * Continuously reads all ADCs for thermistors and current sensing.
    * Generates PWM signals for the Peltier H-bridges and fans.
    * Monitors tachometer feedback to calculate fan RPM.
    * Listens for fault signals from the H-bridge drivers to ensure safe operation.

---
## STM32 Pinout & Peripherals

The following table details the primary pin assignments for the STM32 microcontroller based on the firmware and schematic.

| Function | STM32 Pin | Description |
| :--- | :--- | :--- |
| **Peltier 1 Control** | | |
| Enable (EN) | `PA5` | Enables/Disables the H-Bridge output. |
| Direction (PH) | `PA8` | Controls current direction (Heating/Cooling). |
| nSLEEP | `PA10` | Wakes or sleeps the DRV8701 driver chip. |
| nFAULT (EXTI) | `PA15` | External interrupt input for fault detection. |
| Current Sense (ADC) | `PA4` | Measures current flowing through the Peltier. |
| SNSOUT (Chop Detect) | `PC9` | Input to detect if current chopping is active. |
| **Peltier 2 Control** | | |
| Enable (EN) | `PC3` | Enables/Disables the H-Bridge output. |
| Direction (PH) | `PC2` | Controls current direction (Heating/Cooling). |
| nSLEEP | `PA0` | Wakes or sleeps the DRV8701 driver chip. |
| nFAULT (EXTI) | `PA2` | External interrupt input for fault detection. |
| Current Sense (ADC) | `PA1` | Measures current flowing through the Peltier. |
| SNSOUT (Chop Detect) | `PA3` | Input to detect if current chopping is active. |
| **Sensors (ADC)** | | |
| Thermistor 1 | `PB0` | ADC input for zone 1 temperature. |
| Thermistor 2 | `PB1` | ADC input for zone 2 temperature. |
| Thermistor 3 | `PB2` | ADC input (e.g., water reservoir temp). |
| Thermistor 4 | `PA7` | ADC input (e.g., ambient temp). |
| **Actuators** | | |
| Pump 1 Driver | `PB11` | GPIO output to control the first pump. |
| Pump 2 Driver | `PB14` | GPIO output to control the second pump. |
| Solenoid 1 Driver | `PB15` | GPIO output to control the first solenoid. |
| Solenoid 2 Driver | `PC6` | GPIO output to control the second solenoid. |
| **Fan Control** | | |
| Fan 1 PWM | `PB5` | TIM3_CH2: PWM output for Fan 1 speed. |
| Fan 1 TACH | `PB4` | TIM3_CH1: Input capture for Fan 1 RPM. |
| Fan 2 PWM | `PB7` | TIM3_CH4: PWM output for Fan 2 speed. |
| Fan 2 TACH | `PB6` | TIM8_CH1: Input capture for Fan 2 RPM. |
| Fan 3 PWM | `PB9` | TIM4_CH4: PWM output for Fan 3 speed. |
| **Communication** | | |
| UART TX (to CM5) | `PC4` | Transmits data and responses to the Pi. |
| UART RX (from CM5) | `PC5` | Receives commands from the Pi. |
| **Audio Interface** | | |
| I2S LRCLK | `PA15` | I2S Left/Right Clock (Word Select). |
| I2S SDIN | `PB15` | I2S Serial Data In to the audio amplifier. |
| I2C SCL | `PB8` | I2C Clock for amplifier control. |
| I2C SDA | `PB9` | I2C Data for amplifier control. |

---
## Software Interface (UART API)

The STM32 is controlled by the Raspberry Pi using a serial command set over UART (115200 baud, 8-N-1). All commands should be terminated with a newline character (`\n`).

| Command | Example | Description |
| :--- | :--- | :--- |
| `ping` | `ping` | Checks for connectivity. The STM32 will respond with "pong". |
| `settemp` | `settemp 1 21.5` | Sets the target temperature for a zone (1 or 2) in °C and enables **AUTO** mode. |
| `peltier` | `peltier 1 cool` | Manually overrides a zone (1 or 2) to a specific state: `heat`, `cool`, or `off`. This disables AUTO mode for that zone. |
| `pump` | `pump 2 on` | Turns a pump (1 or 2) `on` or `off`. |
| `solenoid` | `solenoid 1 on` | Turns a solenoid (1 or 2) `on` or `off`. |
| `fan` | `fan 3 75` | Sets a fan's (1-3) speed to a percentage (0-100). |
| `getrpm` | `getrpm 2` | Responds with the current RPM of the specified fan (1 or 2). |
| `therm` | `therm 4` | Responds with the raw ADC value and calculated temperature in Celsius for a thermistor (1-4). |
| `current` | `current 1` | Responds with the raw ADC value from the current sensor for a Peltier zone (1 or 2). |
| `snsout` | `snsout 2` | Reports if current chopping is active for a Peltier zone (1 or 2). |

---
## Build & Deploy Firmware

### Prerequisites

* [STM32CubeIDE](https://www.st.com/en/development-tools/stm32cubeide.html)
* ST-Link programmer/debugger

### Building

1.  Clone this repository.
2.  Open STM32CubeIDE and import the project by navigating to `File > Import... > General > Existing Projects into Workspace`.
3.  Select the cloned repository's root directory.
4.  Build the project using `Project > Build All`.

### Flashing

1.  Connect the ST-Link to the SWD header on the development board.
2.  In STM32CubeIDE, right-click the project and select `Run As > STM32 Application`.
3.  The IDE will automatically build and flash the firmware to the microcontroller.
