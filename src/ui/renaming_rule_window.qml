import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Window 2.0
import QtQuick.Layouts 1.1
import QtQml.Models 2.1

ApplicationWindow {
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

//    function addRule(rule) {
//        rulesList.model.append({ rule: rule })
//    }

//    function removeSelectedRule() {
//        var currentIndex = rulesList.currentIndex
//        console.log(currentIndex)
//    }

//    function removeAllRules() {

//    }


    Rectangle {
        id: root

        width: 500
        height: 100

        ListModel {
            id: listModel
        }

        Component {
            id: dragDelegate

            MouseArea {
                id: dragArea

                anchors {
                    top: parent.top
                    bottom: parent.bottom
                }
                width: content.width

                property bool held: false

                drag.target: held ? content : undefined
                drag.axis: Drag.XAxis

                onPressed: held = true
                onReleased: held = false

                Rectangle {
                    id: content

                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        verticalCenter: parent.verticalCenter
                    }
                    width: label.implicitWidth + 18
                    height: label.implicitHeight + 12

                    border.width: 1
                    border.color: "lightGray"
                    radius: 5
                    color: dragArea.held ? "lightGray" : "white"
                    Behavior on color { ColorAnimation { duration: 100 } }

                    Drag.active: dragArea.held
                    Drag.source: dragArea
                    Drag.hotSpot.x: width / 2
                    Drag.hotSpot.y: height / 2

                    states: State {
                        when: dragArea.held

                        ParentChange { target: content; parent: root }
                        AnchorChanges {
                            target: content
                            anchors { horizontalCenter: undefined; verticalCenter: undefined }
                        }
                    }

                    Label {
                        id: label

                        anchors.centerIn: parent

                        text: name
                        font.pointSize: 18
                    }
                }
                DropArea {
                    anchors.fill: parent

                    onEntered: {
                        visualModel.items.move(
                                    drag.source.DelegateModel.itemsIndex,
                                    dragArea.DelegateModel.itemsIndex)
                    }
                }
            }
        }

        DelegateModel {
            id: visualModel

            model: listModel
            delegate: dragDelegate
        }

        ListView {
            id: view

            anchors { fill: parent }

            orientation: ListView.Horizontal
            model: visualModel
            spacing: 6

            moveDisplaced: Transition {
                NumberAnimation {
                    properties: "x,y"
                    easing.type: Easing.Bezier
                    easing.bezierCurve: [0.4,0.0, 0.2,1.0, 1.0,1.0]
                    duration: 150
                }
            }
        }
    }



//    ColumnLayout {
//        anchors.fill: parent
//        anchors.leftMargin: 11
//        anchors.rightMargin: 11
//        anchors.topMargin: 11
//        anchors.bottomMargin: 11

//        spacing: 6

//        Label {
//            text: "Define renaming rule using movie attributes:"
//        }

//        RowLayout {
//            ListView {
//                id: rulesList
//                Layout.fillWidth: true
//                Layout.fillHeight: true

//                orientation: ListView.Horizontal
//                focus: true

//                delegate: Label {
//                    text: rule
//                }

//                model: ListModel{}
//            }
//            Button {
//                text: "Remove"
//                onClicked: removeRuleClicked()
//            }
//            Button {
//                text: "Clear"
//                onClicked: removeAllRulesClicked()
//            }
//        }

//        GridLayout {
//            columns: 2

//            Button {
//                text: "Title"
//                Layout.row: 1
//                onClicked: addTitleClicked()
//            }

//            Button {
//                text: "Original title"
//                Layout.row: 2
//                onClicked: addOriginalTitleClicked()
//            }

//            Button {
//                text: "Year"
//                Layout.row: 3
//                onClicked: addYearClicked()
//            }

//            Button {
//                text: "Director(s)"
//                Layout.row: 4
//                onClicked: addDirectorsClicked()
//            }

//            Button {
//                text: "Duration"
//                Layout.row: 5
//                onClicked: addDurationClicked()
//            }

//            ComboBox {
//                Layout.row: 5
//                Layout.column: 2
//            }

//            Button {
//                text: "Language"
//                Layout.row: 6
//                onClicked: addLanguageClicked()
//            }

//            Button {
//                text: "(...)"
//                Layout.row: 7
//                onClicked: addRoundBracketsClicked()
//            }

//            Button {
//                text: "[...]"
//                Layout.row: 8
//                onClicked: addSquareBracketsClicked()
//            }

//            Button {
//                text: "{...}"
//                Layout.row: 9
//                onClicked: addCurlyBracketsClicked()
//            }

//            Label {
//                text: "Words are separated with:"
//                Layout.row: 10
//            }

//            ComboBox {
//                Layout.row: 10
//                Layout.column: 2
//            }
//        }

//        Label {
//            text: "Example:"
//        }

//        Label {
//            text: ""
//        }

//        Label {
//            text: "will be renamed into:"
//        }

//        Label {
//            text: ""
//        }

//        RowLayout {
//            Item {
//                Layout.fillWidth: true
//            }
//            Button {
//                text: "Close"
//                onClicked: closeClicked()
//            }
//        }
//    }
}
