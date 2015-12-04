import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Layouts 1.1

Window {
    width: 600
    height: 600
    visible: true

    ColumnLayout {
        anchors.fill: parent

        spacing: 6
        Layout.leftMargin: 11
        Layout.rightMargin: 11
        Layout.topMargin: 11
        Layout.bottomMargin: 11

        Label {
            text: "Define renaming rule using movie attributes:"
        }

        RowLayout {
            ListView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                delegate: Label {

                }
            }
            Button {
                text: "Remove"
            }
            Button {
                text: "Clear"
            }
        }

        GridLayout {
            columns: 2

            Button {
                text: "Title"
                Layout.row: 1
            }

            Button {
                text: "Original title"
                Layout.row: 2
            }

            Button {
                text: "Year"
                Layout.row: 3
            }

            Button {
                text: "Director(s)"
                Layout.row: 4
            }

            Button {
                text: "Duration"
                Layout.row: 5
            }

            ComboBox {
                Layout.row: 5
                Layout.column: 2
            }

            Button {
                text: "Language"
                Layout.row: 6
            }

            Button {
                text: "(...)"
                Layout.row: 7
            }

            Button {
                text: "[...]"
                Layout.row: 8
            }

            Button {
                text: "{...}"
                Layout.row: 9
            }

            Label {
                text: "Words are separated with:"
                Layout.row: 10
            }

            ComboBox {
                Layout.row: 10
                Layout.column: 2
            }
        }

        Label {
            text: "Example:"
        }

        Label {
            text: ""
        }

        Label {
            text: "will be renamed into:"
        }

        Label {
            text: ""
        }
    }
}
