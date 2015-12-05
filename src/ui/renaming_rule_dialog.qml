import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.2

Window {
    width: 600
    height: 520
    visible: true

    title: "Renaming rule"

    signal removeRuleClicked()
    signal removeAllRulesClicked()
    signal addTitleClicked()
    signal addOriginalTitleClicked()
    signal addYearClicked()
    signal addDirectorsClicked()
    signal addDurationClicked()
    signal addLanguageClicked()
    signal addRoundBracketsClicked()
    signal addSquareBracketsClicked()
    signal addCurlyBracketsClicked()
    signal closeClicked()

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
                onClicked: removeRuleClicked()
            }
            Button {
                text: "Clear"
                onClicked: removeAllRulesClicked()
            }
        }

        GridLayout {
            columns: 2

            Button {
                text: "Title"
                Layout.row: 1
                onClicked: addTitleClicked()
            }

            Button {
                text: "Original title"
                Layout.row: 2
                onClicked: addOriginalTitleClicked()
            }

            Button {
                text: "Year"
                Layout.row: 3
                onClicked: addYearClicked()
            }

            Button {
                text: "Director(s)"
                Layout.row: 4
                onClicked: addDirectorsClicked()
            }

            Button {
                text: "Duration"
                Layout.row: 5
                onClicked: addDurationClicked()
            }

            ComboBox {
                Layout.row: 5
                Layout.column: 2
            }

            Button {
                text: "Language"
                Layout.row: 6
                onClicked: addLanguageClicked()
            }

            Button {
                text: "(...)"
                Layout.row: 7
                onClicked: addRoundBracketsClicked()
            }

            Button {
                text: "[...]"
                Layout.row: 8
                onClicked: addSquareBracketsClicked()
            }

            Button {
                text: "{...}"
                Layout.row: 9
                onClicked: addCurlyBracketsClicked()
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

        RowLayout {
            Item {
                Layout.fillWidth: true
            }
            Button {
                text: "Close"
                onClicked: closeClicked()
            }
        }
    }
}
