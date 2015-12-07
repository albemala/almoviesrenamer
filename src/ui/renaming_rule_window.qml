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

    function addRule(rule) {
        rulesListModel.append({ rule: rule })
    }

    function removeSelectedRule() {
        var currentIndex = rulesList.currentIndex
        console.log(currentIndex)
    }

    function removeAllRules() {

    }

    ColumnLayout {
        anchors.fill: parent
        anchors.leftMargin: 11
        anchors.rightMargin: 11
        anchors.topMargin: 11
        anchors.bottomMargin: 11

        spacing: 6

        Label {
            text: "Define renaming rule using movie attributes:"
        }

        RowLayout {
            Rectangle {
                anchors.fill: rulesList
                color: "white"
            }

            ListView {
                id: rulesList

                Layout.fillWidth: true
                Layout.fillHeight: true

                orientation: ListView.Horizontal
                model: rulesListDelegateModel
                spacing: 6

                moveDisplaced: Transition {
                    NumberAnimation {
                        properties: "x,y"
                        easing.type: Easing.Bezier
                        easing.bezierCurve: [0.4,0.0, 0.2,1.0, 1.0,1.0]
                        duration: 150
                    }
                }

                ListModel {
                    id: rulesListModel
                }

                Component {
                    id: rulesListDelegate

                    MouseArea {
                        id: dragArea

                        anchors {
                            top: parent.top
                            bottom: parent.bottom
                        }
                        width: ruleContentBackground.width

                        property bool held: false

                        drag.target: held ? ruleContentBackground : undefined
                        drag.axis: Drag.XAxis

                        onPressed: held = true
                        onReleased: held = false

                        Rectangle {
                            id: ruleContentBackground

                            anchors {
                                horizontalCenter: parent.horizontalCenter
                                verticalCenter: parent.verticalCenter
                            }
                            width: ruleContent.width + 18
                            height: ruleContent.height + 12

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

                                ParentChange { target: ruleContentBackground; parent: rulesList }
                                AnchorChanges {
                                    target: ruleContentBackground
                                    anchors { horizontalCenter: undefined; verticalCenter: undefined }
                                }
                            }

                            RowLayout {
                                id: ruleContent

                                anchors.centerIn: parent
                                width: ruleLabel.implicitWidth + ruleRemoveButton.implicitWidth + spacing
                                height: ruleRemoveButton.implicitHeight

                                spacing: 12


                                Label {
                                    id: ruleLabel

                                    text: rule
                                    font.pointSize: 18
                                }
                                Label {
                                    id: ruleRemoveButton

                                    text: "\u00D7"
                                    font.pointSize: 24
                                    color: darkRed

                                    property string darkRed: "#D84315"
                                    property string lightRed: "#FFAB91"

                                    MouseArea {
                                        anchors.fill: parent

                                        onPressed: {
                                            ruleRemoveButton.color = ruleRemoveButton.lightRed
                                        }
                                        onReleased: {
                                            ruleRemoveButton.color = ruleRemoveButton.darkRed
                                        }
                                        onCanceled: {
                                            ruleRemoveButton.color = ruleRemoveButton.darkRed
                                        }

                                        onClicked: {}
                                    }
                                }
                            }
                        }
                        DropArea {
                            anchors.fill: parent

                            onEntered: {
                                rulesListDelegateModel.items.move(
                                            drag.source.DelegateModel.itemsIndex,
                                            dragArea.DelegateModel.itemsIndex)
                            }
                        }
                    }
                }

                DelegateModel {
                    id: rulesListDelegateModel

                    model: rulesListModel
                    delegate: rulesListDelegate
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
