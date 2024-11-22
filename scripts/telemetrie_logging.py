#!/usr/bin/env python3

import rospy
from mavros_msgs.msg import State, ExtendedState
from sensor_msgs.msg import NavSatFix, Imu, BatteryState  # BatteryState ist hier
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav_msgs.msg import Odometry
import datetime
import os
import json

class TelemetryLogger:
    def __init__(self):
        rospy.init_node('telemetry_logger')

        # Erstelle Logs-Verzeichnis und Logdateien
        self.setup_logging()

        # Dictionary für die verschiedenen Log-Dateien
        self.log_files = {}
        self.setup_log_files()

        # Subscriber einrichten
        self.setup_subscribers()

        rospy.loginfo(f"Telemetrie-Logger gestartet. Logs werden gespeichert in: {self.log_dir}")

    def setup_logging(self):
        # Bestimme Basis-Verzeichnis für Logs
        script_dir = os.path.dirname(os.path.realpath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        self.log_dir = os.path.join(project_root, 'logs',
                                   datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

        # Erstelle Verzeichnis
        os.makedirs(self.log_dir, exist_ok=True)



    def setup_log_files(self):
        log_types = ['state', 'position', 'gps', 'imu', 'battery',
                    'velocity', 'extended_state', 'summary']

        for log_type in log_types:
            file_path = os.path.join(self.log_dir, f'{log_type}.log')
            self.log_files[log_type] = open(file_path, 'w')

    def setup_subscribers(self):
        rospy.Subscriber("/mavros/state", State,
                        lambda msg: self.log_data('state', msg))
        rospy.Subscriber("/mavros/local_position/pose", PoseStamped,
                        lambda msg: self.log_data('position', msg))
        rospy.Subscriber("/mavros/global_position/global", NavSatFix,
                        lambda msg: self.log_data('gps', msg))
        rospy.Subscriber("/mavros/imu/data", Imu,
                        lambda msg: self.log_data('imu', msg))
        rospy.Subscriber("/mavros/battery", BatteryState,
                        lambda msg: self.log_data('battery', msg))
        rospy.Subscriber("/mavros/local_position/velocity_local", TwistStamped,
                        lambda msg: self.log_data('velocity', msg))
        rospy.Subscriber("/mavros/extended_state", ExtendedState,
                        lambda msg: self.log_data('extended_state', msg))

    def log_data(self, log_type, msg):
        timestamp = rospy.Time.now().to_sec()

        try:
            # Daten je nach Typ formatieren
            if log_type == 'state':
                data = {
                    'mode': msg.mode,
                    'armed': msg.armed,
                    'connected': msg.connected
                }
                self.log_summary(f"Statusänderung - Mode: {msg.mode}, Armed: {msg.armed}")

            elif log_type == 'position':
                data = {
                    'position': {
                        'x': msg.pose.position.x,
                        'y': msg.pose.position.y,
                        'z': msg.pose.position.z
                    },
                    'orientation': {
                        'x': msg.pose.orientation.x,
                        'y': msg.pose.orientation.y,
                        'z': msg.pose.orientation.z,
                        'w': msg.pose.orientation.w
                    }
                }

            elif log_type == 'gps':
                data = {
                    'latitude': msg.latitude,
                    'longitude': msg.longitude,
                    'altitude': msg.altitude,
                    'status': msg.status.status
                }

            elif log_type == 'imu':
                data = {
                    'angular_velocity': {
                        'x': msg.angular_velocity.x,
                        'y': msg.angular_velocity.y,
                        'z': msg.angular_velocity.z
                    },
                    'linear_acceleration': {
                        'x': msg.linear_acceleration.x,
                        'y': msg.linear_acceleration.y,
                        'z': msg.linear_acceleration.z
                    }
                }

            elif log_type == 'battery':
                data = {
                    'voltage': msg.voltage,
                    'current': msg.current,
                    'percentage': msg.capacity
                }
                if hasattr(msg, 'percentage') and msg.percentage < 20:
                    self.log_summary(f"WARNUNG: Niedriger Batteriestand: {msg.percentage}%")

            elif log_type == 'velocity':
                data = {
                    'linear': {
                        'x': msg.twist.linear.x,
                        'y': msg.twist.linear.y,
                        'z': msg.twist.linear.z
                    },
                    'angular': {
                        'x': msg.twist.angular.x,
                        'y': msg.twist.angular.y,
                        'z': msg.twist.angular.z
                    }
                }

            elif log_type == 'extended_state':
                data = {
                    'vtol_state': msg.vtol_state,
                    'landed_state': msg.landed_state
                }
                self.log_summary(f"Landed State geändert: {msg.landed_state}")

            # Schreibe formatierte Daten in Log-Datei
            log_entry = f"[{timestamp}] {json.dumps(data)}\n"
            self.log_files[log_type].write(log_entry)
            self.log_files[log_type].flush()

        except Exception as e:
            rospy.logerr(f"Fehler beim Logging von {log_type}: {str(e)}")

    def log_summary(self, message):
        """Loggt wichtige Events in die Summary-Datei"""
        timestamp = rospy.Time.now().to_sec()
        log_entry = f"[{timestamp}] {message}\n"
        self.log_files['summary'].write(log_entry)
        self.log_files['summary'].flush()

    def cleanup(self):
        """Schließt alle Log-Dateien sauber"""
        for file in self.log_files.values():
            file.close()
        rospy.loginfo("Telemetrie-Logger beendet - Alle Dateien geschlossen")

if __name__ == "__main__":
    try:
        logger = TelemetryLogger()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        if 'logger' in locals():
            logger.cleanup()
