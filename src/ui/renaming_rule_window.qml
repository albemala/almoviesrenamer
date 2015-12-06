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

        width: 300; height: 400

        ListModel {
            id: listModel

            ListElement {
                name: "Polly"
            }
            ListElement {
                name: "Penny"
            }
            ListElement {
                name: "Warren"
            }
            ListElement {
                name: "Spot"
            }
            ListElement {
                name: "Joey"
            }
            ListElement {
                name: "Kimba"
            }
        }

        Component {
            id: dragDelegate

            MouseArea {
                id: dragArea

                property bool held: false

                anchors { left: parent.left; right: parent.right }
                height: content.height

                drag.target: held ? content : undefined
                drag.axis: Drag.YAxis

                onPressed: held = true
                onReleased: held = false

                Rectangle {
                    id: content
                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        verticalCenter: parent.verticalCenter
                    }
                    width: dragArea.width; height: column.implicitHeight

                    border.width: 1
                    border.color: "lightsteelblue"

                    color: dragArea.held ? "lightsteelblue" : "white"
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
                        id: column
                        anchors.fill: parent
                        text: 'Name: ' + name
                    }
                }
                DropArea {
                    anchors { fill: parent; margins: 10 }

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

            model: visualModel
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
