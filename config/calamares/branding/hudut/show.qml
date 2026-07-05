import QtQuick 2.0

Rectangle {
    width: 800
    height: 520
    color: "#202833"

    Column {
        anchors.centerIn: parent
        spacing: 18

        Image {
            source: "hudut-logo.png"
            width: 160
            height: 160
            fillMode: Image.PreserveAspectFit
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "Hudut Linux Kurulum"
            color: "white"
            font.pixelSize: 34
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "V0.1 Beta"
            color: "#ff7a00"
            font.pixelSize: 26
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "Secure OSINT Workstation"
            color: "white"
            font.pixelSize: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "Yasal OSINT, CTI, GEOINT ve güvenli araştırma ortamı."
            color: "white"
            font.pixelSize: 16
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
