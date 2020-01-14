/********************************************************************************
** Form generated from reading UI file 'roar.ui'
**
** Created by: Qt User Interface Compiler version 5.12.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ROAR_H
#define UI_ROAR_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_canvas
{
public:
    QAction *actionNew;
    QAction *actionOpen;
    QAction *actionSave;
    QAction *actionSaveAs;
    QAction *actionExit;
    QAction *actionUndo;
    QAction *actionRedo;
    QAction *actionCut;
    QAction *actionCopy;
    QAction *actionPaste;
    QAction *actionDelete;
    QAction *actionSolidBrush;
    QAction *actionHideAssetsWindow;
    QAction *actionShowAssetsWindow;
    QAction *actionCursor;
    QAction *actionRectangle;
    QAction *actionCircle;
    QAction *actionFill;
    QAction *actionLine;
    QAction *actionText;
    QAction *actionObject;
    QAction *actionErase;
    QAction *actionPickColour;
    QAction *actionFlip;
    QAction *actionFlipHorizontally;
    QAction *actionInvertColours;
    QAction *actionRotate;
    QAction *actionTile;
    QAction *actionViewMelp;
    QAction *actionOpenIssueOnGitHub;
    QAction *actionVisitGitHubWebsite;
    QAction *actionAboutRoar;
    QAction *actionColour00;
    QAction *actionColour01;
    QAction *actionColour02;
    QAction *actionColour03;
    QAction *actionColour04;
    QAction *actionColour05;
    QAction *actionColour06;
    QAction *actionColour07;
    QAction *actionColour08;
    QAction *actionColour09;
    QAction *actionColour10;
    QAction *actionColour11;
    QAction *actionColour12;
    QAction *actionColour13;
    QAction *actionColour14;
    QAction *actionColour15;
    QAction *actionColourTransparent;
    QAction *actionColourBg00;
    QAction *actionColourBg01;
    QAction *actionColourBg02;
    QAction *actionColourBg03;
    QAction *actionColourBg04;
    QAction *actionColourBg05;
    QAction *actionColourBg06;
    QAction *actionColourBg07;
    QAction *actionColourBg08;
    QAction *actionColourBg09;
    QAction *actionColourBg10;
    QAction *actionColourBg11;
    QAction *actionColourBg12;
    QAction *actionColourBg13;
    QAction *actionColourBg14;
    QAction *actionColourBg15;
    QAction *actionColourBgTransparent;
    QAction *actionIncreaseBrushWidth;
    QAction *actionDecreaseBrushWidth;
    QAction *actionIncreaseBrushHeight;
    QAction *actionDecreaseBrushHeight;
    QAction *actionIncreaseBrushSize;
    QAction *actionDecreaseBrushSize;
    QAction *actionIncreaseCanvasWidth;
    QAction *actionDecreaseCanvasWidth;
    QAction *actionIncreaseCanvasHeight;
    QAction *actionDecreaseCanvasHeight;
    QAction *actionIncreaseCanvasSize;
    QAction *actionDecreaseCanvasSize;
    QAction *actionDecreaseCellSize;
    QAction *actionIncreaseCellSize;
    QAction *actionExportAsANSI;
    QAction *actionExportToClipboard;
    QAction *actionExportToImgur;
    QAction *actionExportToPastebin;
    QAction *actionExportAsPNG;
    QAction *actionImportANSI;
    QAction *actionImportFromClipboard;
    QAction *actionImportSAUCE;
    QAction *actionFlipColours;
    QAction *action_Clear_list;
    QAction *actionRestore_from_file;
    QWidget *centralwidget;
    QWidget *verticalLayoutWidget;
    QVBoxLayout *verticalLayout;
    QMenuBar *menubar;
    QMenu *menuFile;
    QMenu *menu_Export;
    QMenu *menu_Import;
    QMenu *menuOpen_Recent;
    QMenu *menuRes_tore_Snapshot;
    QMenu *menuEdit;
    QMenu *menuBrush_size;
    QMenu *menuCanvas_size;
    QMenu *menuTools;
    QMenu *menuOperators;
    QMenu *menuHelp;
    QStatusBar *statusbar;
    QToolBar *toolBarCommands;
    QToolBar *toolBarTools;
    QToolBar *toolBarColours;
    QToolBar *toolBarColoursBackground;

    void setupUi(QMainWindow *canvas)
    {
        if (canvas->objectName().isEmpty())
            canvas->setObjectName(QString::fromUtf8("canvas"));
        canvas->resize(840, 640);
        actionNew = new QAction(canvas);
        actionNew->setObjectName(QString::fromUtf8("actionNew"));
        QIcon icon;
        icon.addFile(QString::fromUtf8("assets/images/document-new.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionNew->setIcon(icon);
        actionOpen = new QAction(canvas);
        actionOpen->setObjectName(QString::fromUtf8("actionOpen"));
        QIcon icon1;
        icon1.addFile(QString::fromUtf8("assets/images/document-open-data.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionOpen->setIcon(icon1);
        actionSave = new QAction(canvas);
        actionSave->setObjectName(QString::fromUtf8("actionSave"));
        QIcon icon2;
        icon2.addFile(QString::fromUtf8("assets/images/document-save.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionSave->setIcon(icon2);
        actionSaveAs = new QAction(canvas);
        actionSaveAs->setObjectName(QString::fromUtf8("actionSaveAs"));
        QIcon icon3;
        icon3.addFile(QString::fromUtf8("assets/images/document-save-as.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionSaveAs->setIcon(icon3);
        actionExit = new QAction(canvas);
        actionExit->setObjectName(QString::fromUtf8("actionExit"));
        actionUndo = new QAction(canvas);
        actionUndo->setObjectName(QString::fromUtf8("actionUndo"));
        actionUndo->setEnabled(false);
        QIcon icon4;
        icon4.addFile(QString::fromUtf8("assets/images/edit-undo.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionUndo->setIcon(icon4);
        actionRedo = new QAction(canvas);
        actionRedo->setObjectName(QString::fromUtf8("actionRedo"));
        actionRedo->setEnabled(false);
        QIcon icon5;
        icon5.addFile(QString::fromUtf8("assets/images/edit-redo.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionRedo->setIcon(icon5);
        actionCut = new QAction(canvas);
        actionCut->setObjectName(QString::fromUtf8("actionCut"));
        actionCut->setEnabled(false);
        QIcon icon6;
        icon6.addFile(QString::fromUtf8("assets/images/edit-cut.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionCut->setIcon(icon6);
        actionCopy = new QAction(canvas);
        actionCopy->setObjectName(QString::fromUtf8("actionCopy"));
        actionCopy->setEnabled(false);
        QIcon icon7;
        icon7.addFile(QString::fromUtf8("assets/images/edit-copy.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionCopy->setIcon(icon7);
        actionPaste = new QAction(canvas);
        actionPaste->setObjectName(QString::fromUtf8("actionPaste"));
        actionPaste->setEnabled(false);
        QIcon icon8;
        icon8.addFile(QString::fromUtf8("assets/images/edit-paste.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionPaste->setIcon(icon8);
        actionDelete = new QAction(canvas);
        actionDelete->setObjectName(QString::fromUtf8("actionDelete"));
        actionDelete->setEnabled(false);
        QIcon icon9;
        icon9.addFile(QString::fromUtf8("assets/images/edit-delete.svg"), QSize(), QIcon::Normal, QIcon::Off);
        actionDelete->setIcon(icon9);
        actionSolidBrush = new QAction(canvas);
        actionSolidBrush->setObjectName(QString::fromUtf8("actionSolidBrush"));
        actionSolidBrush->setCheckable(true);
        actionSolidBrush->setChecked(true);
        actionHideAssetsWindow = new QAction(canvas);
        actionHideAssetsWindow->setObjectName(QString::fromUtf8("actionHideAssetsWindow"));
        actionHideAssetsWindow->setEnabled(false);
        QIcon icon10;
        icon10.addFile(QString::fromUtf8("assets/images/toolHideAssetsWindow.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionHideAssetsWindow->setIcon(icon10);
        actionShowAssetsWindow = new QAction(canvas);
        actionShowAssetsWindow->setObjectName(QString::fromUtf8("actionShowAssetsWindow"));
        actionShowAssetsWindow->setEnabled(false);
        QIcon icon11;
        icon11.addFile(QString::fromUtf8("assets/images/toolShowAssetsWindow.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionShowAssetsWindow->setIcon(icon11);
        actionCursor = new QAction(canvas);
        actionCursor->setObjectName(QString::fromUtf8("actionCursor"));
        actionCursor->setCheckable(true);
        QIcon icon12;
        icon12.addFile(QString::fromUtf8("assets/images/toolCursor.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionCursor->setIcon(icon12);
        actionRectangle = new QAction(canvas);
        actionRectangle->setObjectName(QString::fromUtf8("actionRectangle"));
        actionRectangle->setCheckable(true);
        QIcon icon13;
        icon13.addFile(QString::fromUtf8("assets/images/toolRect.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionRectangle->setIcon(icon13);
        actionCircle = new QAction(canvas);
        actionCircle->setObjectName(QString::fromUtf8("actionCircle"));
        actionCircle->setCheckable(true);
        QIcon icon14;
        icon14.addFile(QString::fromUtf8("assets/images/toolCircle.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionCircle->setIcon(icon14);
        actionFill = new QAction(canvas);
        actionFill->setObjectName(QString::fromUtf8("actionFill"));
        actionFill->setCheckable(true);
        QIcon icon15;
        icon15.addFile(QString::fromUtf8("assets/images/toolFill.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionFill->setIcon(icon15);
        actionLine = new QAction(canvas);
        actionLine->setObjectName(QString::fromUtf8("actionLine"));
        actionLine->setCheckable(true);
        QIcon icon16;
        icon16.addFile(QString::fromUtf8("assets/images/toolLine.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionLine->setIcon(icon16);
        actionText = new QAction(canvas);
        actionText->setObjectName(QString::fromUtf8("actionText"));
        actionText->setCheckable(true);
        QIcon icon17;
        icon17.addFile(QString::fromUtf8("assets/images/toolText.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionText->setIcon(icon17);
        actionObject = new QAction(canvas);
        actionObject->setObjectName(QString::fromUtf8("actionObject"));
        actionObject->setCheckable(true);
        QIcon icon18;
        icon18.addFile(QString::fromUtf8("assets/images/toolObject.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionObject->setIcon(icon18);
        actionErase = new QAction(canvas);
        actionErase->setObjectName(QString::fromUtf8("actionErase"));
        actionErase->setCheckable(true);
        QIcon icon19;
        icon19.addFile(QString::fromUtf8("assets/images/toolErase.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionErase->setIcon(icon19);
        actionPickColour = new QAction(canvas);
        actionPickColour->setObjectName(QString::fromUtf8("actionPickColour"));
        actionPickColour->setCheckable(true);
        QIcon icon20;
        icon20.addFile(QString::fromUtf8("assets/images/toolPickColour.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionPickColour->setIcon(icon20);
        actionFlip = new QAction(canvas);
        actionFlip->setObjectName(QString::fromUtf8("actionFlip"));
        actionFlip->setCheckable(true);
        actionFlip->setEnabled(true);
        actionFlipHorizontally = new QAction(canvas);
        actionFlipHorizontally->setObjectName(QString::fromUtf8("actionFlipHorizontally"));
        actionFlipHorizontally->setCheckable(true);
        actionInvertColours = new QAction(canvas);
        actionInvertColours->setObjectName(QString::fromUtf8("actionInvertColours"));
        actionInvertColours->setCheckable(true);
        actionRotate = new QAction(canvas);
        actionRotate->setObjectName(QString::fromUtf8("actionRotate"));
        actionRotate->setCheckable(true);
        actionTile = new QAction(canvas);
        actionTile->setObjectName(QString::fromUtf8("actionTile"));
        actionTile->setCheckable(true);
        actionViewMelp = new QAction(canvas);
        actionViewMelp->setObjectName(QString::fromUtf8("actionViewMelp"));
        actionOpenIssueOnGitHub = new QAction(canvas);
        actionOpenIssueOnGitHub->setObjectName(QString::fromUtf8("actionOpenIssueOnGitHub"));
        actionVisitGitHubWebsite = new QAction(canvas);
        actionVisitGitHubWebsite->setObjectName(QString::fromUtf8("actionVisitGitHubWebsite"));
        actionAboutRoar = new QAction(canvas);
        actionAboutRoar->setObjectName(QString::fromUtf8("actionAboutRoar"));
        actionColour00 = new QAction(canvas);
        actionColour00->setObjectName(QString::fromUtf8("actionColour00"));
        actionColour00->setCheckable(true);
        QIcon icon21;
        icon21.addFile(QString::fromUtf8("assets/images/colour00.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour00->setIcon(icon21);
        actionColour01 = new QAction(canvas);
        actionColour01->setObjectName(QString::fromUtf8("actionColour01"));
        actionColour01->setCheckable(true);
        QIcon icon22;
        icon22.addFile(QString::fromUtf8("assets/images/colour01.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour01->setIcon(icon22);
        actionColour02 = new QAction(canvas);
        actionColour02->setObjectName(QString::fromUtf8("actionColour02"));
        actionColour02->setCheckable(true);
        QIcon icon23;
        icon23.addFile(QString::fromUtf8("assets/images/colour02.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour02->setIcon(icon23);
        actionColour03 = new QAction(canvas);
        actionColour03->setObjectName(QString::fromUtf8("actionColour03"));
        actionColour03->setCheckable(true);
        QIcon icon24;
        icon24.addFile(QString::fromUtf8("assets/images/colour03.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour03->setIcon(icon24);
        actionColour04 = new QAction(canvas);
        actionColour04->setObjectName(QString::fromUtf8("actionColour04"));
        actionColour04->setCheckable(true);
        QIcon icon25;
        icon25.addFile(QString::fromUtf8("assets/images/colour04.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour04->setIcon(icon25);
        actionColour05 = new QAction(canvas);
        actionColour05->setObjectName(QString::fromUtf8("actionColour05"));
        actionColour05->setCheckable(true);
        QIcon icon26;
        icon26.addFile(QString::fromUtf8("assets/images/colour05.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour05->setIcon(icon26);
        actionColour06 = new QAction(canvas);
        actionColour06->setObjectName(QString::fromUtf8("actionColour06"));
        actionColour06->setCheckable(true);
        QIcon icon27;
        icon27.addFile(QString::fromUtf8("assets/images/colour06.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour06->setIcon(icon27);
        actionColour07 = new QAction(canvas);
        actionColour07->setObjectName(QString::fromUtf8("actionColour07"));
        actionColour07->setCheckable(true);
        QIcon icon28;
        icon28.addFile(QString::fromUtf8("assets/images/colour07.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour07->setIcon(icon28);
        actionColour08 = new QAction(canvas);
        actionColour08->setObjectName(QString::fromUtf8("actionColour08"));
        actionColour08->setCheckable(true);
        QIcon icon29;
        icon29.addFile(QString::fromUtf8("assets/images/colour08.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour08->setIcon(icon29);
        actionColour09 = new QAction(canvas);
        actionColour09->setObjectName(QString::fromUtf8("actionColour09"));
        actionColour09->setCheckable(true);
        QIcon icon30;
        icon30.addFile(QString::fromUtf8("assets/images/colour09.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour09->setIcon(icon30);
        actionColour10 = new QAction(canvas);
        actionColour10->setObjectName(QString::fromUtf8("actionColour10"));
        actionColour10->setCheckable(true);
        QIcon icon31;
        icon31.addFile(QString::fromUtf8("assets/images/colour10.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour10->setIcon(icon31);
        actionColour11 = new QAction(canvas);
        actionColour11->setObjectName(QString::fromUtf8("actionColour11"));
        actionColour11->setCheckable(true);
        QIcon icon32;
        icon32.addFile(QString::fromUtf8("assets/images/colour11.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour11->setIcon(icon32);
        actionColour12 = new QAction(canvas);
        actionColour12->setObjectName(QString::fromUtf8("actionColour12"));
        actionColour12->setCheckable(true);
        QIcon icon33;
        icon33.addFile(QString::fromUtf8("assets/images/colour12.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour12->setIcon(icon33);
        actionColour13 = new QAction(canvas);
        actionColour13->setObjectName(QString::fromUtf8("actionColour13"));
        actionColour13->setCheckable(true);
        QIcon icon34;
        icon34.addFile(QString::fromUtf8("assets/images/colour13.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour13->setIcon(icon34);
        actionColour14 = new QAction(canvas);
        actionColour14->setObjectName(QString::fromUtf8("actionColour14"));
        actionColour14->setCheckable(true);
        QIcon icon35;
        icon35.addFile(QString::fromUtf8("assets/images/colour14.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour14->setIcon(icon35);
        actionColour15 = new QAction(canvas);
        actionColour15->setObjectName(QString::fromUtf8("actionColour15"));
        actionColour15->setCheckable(true);
        QIcon icon36;
        icon36.addFile(QString::fromUtf8("assets/images/colour15.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColour15->setIcon(icon36);
        actionColourTransparent = new QAction(canvas);
        actionColourTransparent->setObjectName(QString::fromUtf8("actionColourTransparent"));
        actionColourTransparent->setCheckable(true);
        QIcon icon37;
        icon37.addFile(QString::fromUtf8("assets/images/colour_transparent.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourTransparent->setIcon(icon37);
        actionColourBg00 = new QAction(canvas);
        actionColourBg00->setObjectName(QString::fromUtf8("actionColourBg00"));
        actionColourBg00->setCheckable(true);
        QIcon icon38;
        icon38.addFile(QString::fromUtf8("assets/images/colourBg00.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg00->setIcon(icon38);
        actionColourBg01 = new QAction(canvas);
        actionColourBg01->setObjectName(QString::fromUtf8("actionColourBg01"));
        actionColourBg01->setCheckable(true);
        QIcon icon39;
        icon39.addFile(QString::fromUtf8("assets/images/colourBg01.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg01->setIcon(icon39);
        actionColourBg02 = new QAction(canvas);
        actionColourBg02->setObjectName(QString::fromUtf8("actionColourBg02"));
        actionColourBg02->setCheckable(true);
        QIcon icon40;
        icon40.addFile(QString::fromUtf8("assets/images/colourBg02.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg02->setIcon(icon40);
        actionColourBg03 = new QAction(canvas);
        actionColourBg03->setObjectName(QString::fromUtf8("actionColourBg03"));
        actionColourBg03->setCheckable(true);
        QIcon icon41;
        icon41.addFile(QString::fromUtf8("assets/images/colourBg03.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg03->setIcon(icon41);
        actionColourBg04 = new QAction(canvas);
        actionColourBg04->setObjectName(QString::fromUtf8("actionColourBg04"));
        actionColourBg04->setCheckable(true);
        QIcon icon42;
        icon42.addFile(QString::fromUtf8("assets/images/colourBg04.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg04->setIcon(icon42);
        actionColourBg05 = new QAction(canvas);
        actionColourBg05->setObjectName(QString::fromUtf8("actionColourBg05"));
        actionColourBg05->setCheckable(true);
        QIcon icon43;
        icon43.addFile(QString::fromUtf8("assets/images/colourBg05.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg05->setIcon(icon43);
        actionColourBg06 = new QAction(canvas);
        actionColourBg06->setObjectName(QString::fromUtf8("actionColourBg06"));
        actionColourBg06->setCheckable(true);
        QIcon icon44;
        icon44.addFile(QString::fromUtf8("assets/images/colourBg06.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg06->setIcon(icon44);
        actionColourBg07 = new QAction(canvas);
        actionColourBg07->setObjectName(QString::fromUtf8("actionColourBg07"));
        actionColourBg07->setCheckable(true);
        QIcon icon45;
        icon45.addFile(QString::fromUtf8("assets/images/colourBg07.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg07->setIcon(icon45);
        actionColourBg08 = new QAction(canvas);
        actionColourBg08->setObjectName(QString::fromUtf8("actionColourBg08"));
        actionColourBg08->setCheckable(true);
        QIcon icon46;
        icon46.addFile(QString::fromUtf8("assets/images/colourBg08.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg08->setIcon(icon46);
        actionColourBg09 = new QAction(canvas);
        actionColourBg09->setObjectName(QString::fromUtf8("actionColourBg09"));
        actionColourBg09->setCheckable(true);
        QIcon icon47;
        icon47.addFile(QString::fromUtf8("assets/images/colourBg09.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg09->setIcon(icon47);
        actionColourBg10 = new QAction(canvas);
        actionColourBg10->setObjectName(QString::fromUtf8("actionColourBg10"));
        actionColourBg10->setCheckable(true);
        QIcon icon48;
        icon48.addFile(QString::fromUtf8("assets/images/colourBg10.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg10->setIcon(icon48);
        actionColourBg11 = new QAction(canvas);
        actionColourBg11->setObjectName(QString::fromUtf8("actionColourBg11"));
        actionColourBg11->setCheckable(true);
        QIcon icon49;
        icon49.addFile(QString::fromUtf8("assets/images/colourBg11.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg11->setIcon(icon49);
        actionColourBg12 = new QAction(canvas);
        actionColourBg12->setObjectName(QString::fromUtf8("actionColourBg12"));
        actionColourBg12->setCheckable(true);
        QIcon icon50;
        icon50.addFile(QString::fromUtf8("assets/images/colourBg12.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg12->setIcon(icon50);
        actionColourBg13 = new QAction(canvas);
        actionColourBg13->setObjectName(QString::fromUtf8("actionColourBg13"));
        actionColourBg13->setCheckable(true);
        QIcon icon51;
        icon51.addFile(QString::fromUtf8("assets/images/colourBg13.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg13->setIcon(icon51);
        actionColourBg14 = new QAction(canvas);
        actionColourBg14->setObjectName(QString::fromUtf8("actionColourBg14"));
        actionColourBg14->setCheckable(true);
        QIcon icon52;
        icon52.addFile(QString::fromUtf8("assets/images/colourBg14.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg14->setIcon(icon52);
        actionColourBg15 = new QAction(canvas);
        actionColourBg15->setObjectName(QString::fromUtf8("actionColourBg15"));
        actionColourBg15->setCheckable(true);
        QIcon icon53;
        icon53.addFile(QString::fromUtf8("assets/images/colourBg15.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBg15->setIcon(icon53);
        actionColourBgTransparent = new QAction(canvas);
        actionColourBgTransparent->setObjectName(QString::fromUtf8("actionColourBgTransparent"));
        actionColourBgTransparent->setCheckable(true);
        QIcon icon54;
        icon54.addFile(QString::fromUtf8("assets/images/colourBg_transparent.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionColourBgTransparent->setIcon(icon54);
        actionIncreaseBrushWidth = new QAction(canvas);
        actionIncreaseBrushWidth->setObjectName(QString::fromUtf8("actionIncreaseBrushWidth"));
        QIcon icon55;
        icon55.addFile(QString::fromUtf8("assets/images/toolIncrBrushW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseBrushWidth->setIcon(icon55);
        actionDecreaseBrushWidth = new QAction(canvas);
        actionDecreaseBrushWidth->setObjectName(QString::fromUtf8("actionDecreaseBrushWidth"));
        QIcon icon56;
        icon56.addFile(QString::fromUtf8("assets/images/toolDecrBrushW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseBrushWidth->setIcon(icon56);
        actionIncreaseBrushHeight = new QAction(canvas);
        actionIncreaseBrushHeight->setObjectName(QString::fromUtf8("actionIncreaseBrushHeight"));
        QIcon icon57;
        icon57.addFile(QString::fromUtf8("assets/images/toolIncrBrushH.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseBrushHeight->setIcon(icon57);
        actionDecreaseBrushHeight = new QAction(canvas);
        actionDecreaseBrushHeight->setObjectName(QString::fromUtf8("actionDecreaseBrushHeight"));
        QIcon icon58;
        icon58.addFile(QString::fromUtf8("assets/images/toolDecrBrushH.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseBrushHeight->setIcon(icon58);
        actionIncreaseBrushSize = new QAction(canvas);
        actionIncreaseBrushSize->setObjectName(QString::fromUtf8("actionIncreaseBrushSize"));
        QIcon icon59;
        icon59.addFile(QString::fromUtf8("assets/images/toolIncrBrushHW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseBrushSize->setIcon(icon59);
        actionDecreaseBrushSize = new QAction(canvas);
        actionDecreaseBrushSize->setObjectName(QString::fromUtf8("actionDecreaseBrushSize"));
        QIcon icon60;
        icon60.addFile(QString::fromUtf8("assets/images/toolDecrBrushHW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseBrushSize->setIcon(icon60);
        actionIncreaseCanvasWidth = new QAction(canvas);
        actionIncreaseCanvasWidth->setObjectName(QString::fromUtf8("actionIncreaseCanvasWidth"));
        QIcon icon61;
        icon61.addFile(QString::fromUtf8("assets/images/toolIncrCanvasW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseCanvasWidth->setIcon(icon61);
        actionDecreaseCanvasWidth = new QAction(canvas);
        actionDecreaseCanvasWidth->setObjectName(QString::fromUtf8("actionDecreaseCanvasWidth"));
        QIcon icon62;
        icon62.addFile(QString::fromUtf8("assets/images/toolDecrCanvasW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseCanvasWidth->setIcon(icon62);
        actionIncreaseCanvasHeight = new QAction(canvas);
        actionIncreaseCanvasHeight->setObjectName(QString::fromUtf8("actionIncreaseCanvasHeight"));
        QIcon icon63;
        icon63.addFile(QString::fromUtf8("assets/images/toolIncrCanvasH.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseCanvasHeight->setIcon(icon63);
        actionDecreaseCanvasHeight = new QAction(canvas);
        actionDecreaseCanvasHeight->setObjectName(QString::fromUtf8("actionDecreaseCanvasHeight"));
        QIcon icon64;
        icon64.addFile(QString::fromUtf8("assets/images/toolDecrCanvasH.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseCanvasHeight->setIcon(icon64);
        actionIncreaseCanvasSize = new QAction(canvas);
        actionIncreaseCanvasSize->setObjectName(QString::fromUtf8("actionIncreaseCanvasSize"));
        QIcon icon65;
        icon65.addFile(QString::fromUtf8("assets/images/toolIncrCanvasHW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionIncreaseCanvasSize->setIcon(icon65);
        actionDecreaseCanvasSize = new QAction(canvas);
        actionDecreaseCanvasSize->setObjectName(QString::fromUtf8("actionDecreaseCanvasSize"));
        QIcon icon66;
        icon66.addFile(QString::fromUtf8("assets/images/toolDecrCanvasHW.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionDecreaseCanvasSize->setIcon(icon66);
        actionDecreaseCellSize = new QAction(canvas);
        actionDecreaseCellSize->setObjectName(QString::fromUtf8("actionDecreaseCellSize"));
        actionIncreaseCellSize = new QAction(canvas);
        actionIncreaseCellSize->setObjectName(QString::fromUtf8("actionIncreaseCellSize"));
        actionExportAsANSI = new QAction(canvas);
        actionExportAsANSI->setObjectName(QString::fromUtf8("actionExportAsANSI"));
        actionExportToClipboard = new QAction(canvas);
        actionExportToClipboard->setObjectName(QString::fromUtf8("actionExportToClipboard"));
        actionExportToImgur = new QAction(canvas);
        actionExportToImgur->setObjectName(QString::fromUtf8("actionExportToImgur"));
        actionExportToPastebin = new QAction(canvas);
        actionExportToPastebin->setObjectName(QString::fromUtf8("actionExportToPastebin"));
        actionExportAsPNG = new QAction(canvas);
        actionExportAsPNG->setObjectName(QString::fromUtf8("actionExportAsPNG"));
        actionImportANSI = new QAction(canvas);
        actionImportANSI->setObjectName(QString::fromUtf8("actionImportANSI"));
        actionImportFromClipboard = new QAction(canvas);
        actionImportFromClipboard->setObjectName(QString::fromUtf8("actionImportFromClipboard"));
        actionImportSAUCE = new QAction(canvas);
        actionImportSAUCE->setObjectName(QString::fromUtf8("actionImportSAUCE"));
        actionFlipColours = new QAction(canvas);
        actionFlipColours->setObjectName(QString::fromUtf8("actionFlipColours"));
        QIcon icon67;
        icon67.addFile(QString::fromUtf8("assets/images/toolColoursFlip.png"), QSize(), QIcon::Normal, QIcon::Off);
        actionFlipColours->setIcon(icon67);
        action_Clear_list = new QAction(canvas);
        action_Clear_list->setObjectName(QString::fromUtf8("action_Clear_list"));
        actionRestore_from_file = new QAction(canvas);
        actionRestore_from_file->setObjectName(QString::fromUtf8("actionRestore_from_file"));
        centralwidget = new QWidget(canvas);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        verticalLayoutWidget = new QWidget(centralwidget);
        verticalLayoutWidget->setObjectName(QString::fromUtf8("verticalLayoutWidget"));
        verticalLayoutWidget->setGeometry(QRect(0, 0, 771, 531));
        verticalLayout = new QVBoxLayout(verticalLayoutWidget);
        verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
        verticalLayout->setContentsMargins(0, 0, 0, 0);
        canvas->setCentralWidget(centralwidget);
        menubar = new QMenuBar(canvas);
        menubar->setObjectName(QString::fromUtf8("menubar"));
        menubar->setGeometry(QRect(0, 0, 840, 21));
        menuFile = new QMenu(menubar);
        menuFile->setObjectName(QString::fromUtf8("menuFile"));
        menu_Export = new QMenu(menuFile);
        menu_Export->setObjectName(QString::fromUtf8("menu_Export"));
        menu_Import = new QMenu(menuFile);
        menu_Import->setObjectName(QString::fromUtf8("menu_Import"));
        menuOpen_Recent = new QMenu(menuFile);
        menuOpen_Recent->setObjectName(QString::fromUtf8("menuOpen_Recent"));
        menuOpen_Recent->setEnabled(false);
        menuRes_tore_Snapshot = new QMenu(menuFile);
        menuRes_tore_Snapshot->setObjectName(QString::fromUtf8("menuRes_tore_Snapshot"));
        menuRes_tore_Snapshot->setEnabled(false);
        menuEdit = new QMenu(menubar);
        menuEdit->setObjectName(QString::fromUtf8("menuEdit"));
        menuBrush_size = new QMenu(menuEdit);
        menuBrush_size->setObjectName(QString::fromUtf8("menuBrush_size"));
        menuCanvas_size = new QMenu(menuEdit);
        menuCanvas_size->setObjectName(QString::fromUtf8("menuCanvas_size"));
        menuTools = new QMenu(menubar);
        menuTools->setObjectName(QString::fromUtf8("menuTools"));
        menuOperators = new QMenu(menubar);
        menuOperators->setObjectName(QString::fromUtf8("menuOperators"));
        menuHelp = new QMenu(menubar);
        menuHelp->setObjectName(QString::fromUtf8("menuHelp"));
        canvas->setMenuBar(menubar);
        statusbar = new QStatusBar(canvas);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        canvas->setStatusBar(statusbar);
        toolBarCommands = new QToolBar(canvas);
        toolBarCommands->setObjectName(QString::fromUtf8("toolBarCommands"));
        canvas->addToolBar(Qt::RightToolBarArea, toolBarCommands);
        toolBarTools = new QToolBar(canvas);
        toolBarTools->setObjectName(QString::fromUtf8("toolBarTools"));
        canvas->addToolBar(Qt::RightToolBarArea, toolBarTools);
        canvas->insertToolBarBreak(toolBarTools);
        toolBarColours = new QToolBar(canvas);
        toolBarColours->setObjectName(QString::fromUtf8("toolBarColours"));
        canvas->addToolBar(Qt::TopToolBarArea, toolBarColours);
        toolBarColoursBackground = new QToolBar(canvas);
        toolBarColoursBackground->setObjectName(QString::fromUtf8("toolBarColoursBackground"));
        canvas->addToolBar(Qt::TopToolBarArea, toolBarColoursBackground);
        canvas->insertToolBarBreak(toolBarColoursBackground);

        menubar->addAction(menuFile->menuAction());
        menubar->addAction(menuEdit->menuAction());
        menubar->addAction(menuTools->menuAction());
        menubar->addAction(menuOperators->menuAction());
        menubar->addAction(menuHelp->menuAction());
        menuFile->addAction(actionNew);
        menuFile->addAction(actionOpen);
        menuFile->addAction(menuOpen_Recent->menuAction());
        menuFile->addAction(menuRes_tore_Snapshot->menuAction());
        menuFile->addAction(actionSave);
        menuFile->addAction(actionSaveAs);
        menuFile->addSeparator();
        menuFile->addAction(menu_Export->menuAction());
        menuFile->addAction(menu_Import->menuAction());
        menuFile->addSeparator();
        menuFile->addAction(actionExit);
        menu_Export->addAction(actionExportAsANSI);
        menu_Export->addAction(actionExportToClipboard);
        menu_Export->addAction(actionExportToImgur);
        menu_Export->addAction(actionExportToPastebin);
        menu_Export->addAction(actionExportAsPNG);
        menu_Import->addAction(actionImportANSI);
        menu_Import->addAction(actionImportFromClipboard);
        menu_Import->addAction(actionImportSAUCE);
        menuOpen_Recent->addAction(action_Clear_list);
        menuRes_tore_Snapshot->addAction(actionRestore_from_file);
        menuEdit->addAction(actionUndo);
        menuEdit->addAction(actionRedo);
        menuEdit->addSeparator();
        menuEdit->addAction(actionCut);
        menuEdit->addAction(actionCopy);
        menuEdit->addAction(actionPaste);
        menuEdit->addAction(actionDelete);
        menuEdit->addSeparator();
        menuEdit->addAction(menuBrush_size->menuAction());
        menuEdit->addAction(menuCanvas_size->menuAction());
        menuEdit->addAction(actionFlipColours);
        menuEdit->addSeparator();
        menuEdit->addAction(actionSolidBrush);
        menuEdit->addSeparator();
        menuEdit->addAction(actionHideAssetsWindow);
        menuEdit->addAction(actionShowAssetsWindow);
        menuBrush_size->addAction(actionIncreaseBrushWidth);
        menuBrush_size->addAction(actionDecreaseBrushWidth);
        menuBrush_size->addAction(actionIncreaseBrushHeight);
        menuBrush_size->addAction(actionDecreaseBrushHeight);
        menuBrush_size->addSeparator();
        menuBrush_size->addAction(actionIncreaseBrushSize);
        menuBrush_size->addAction(actionDecreaseBrushSize);
        menuCanvas_size->addAction(actionIncreaseCanvasWidth);
        menuCanvas_size->addAction(actionDecreaseCanvasWidth);
        menuCanvas_size->addAction(actionIncreaseCanvasHeight);
        menuCanvas_size->addAction(actionDecreaseCanvasHeight);
        menuCanvas_size->addSeparator();
        menuCanvas_size->addAction(actionIncreaseCanvasSize);
        menuCanvas_size->addAction(actionDecreaseCanvasSize);
        menuTools->addAction(actionCursor);
        menuTools->addAction(actionRectangle);
        menuTools->addAction(actionCircle);
        menuTools->addAction(actionFill);
        menuTools->addAction(actionLine);
        menuTools->addAction(actionText);
        menuTools->addAction(actionObject);
        menuTools->addAction(actionErase);
        menuTools->addAction(actionPickColour);
        menuOperators->addAction(actionFlip);
        menuOperators->addAction(actionFlipHorizontally);
        menuOperators->addAction(actionInvertColours);
        menuOperators->addAction(actionRotate);
        menuOperators->addAction(actionTile);
        menuHelp->addAction(actionViewMelp);
        menuHelp->addSeparator();
        menuHelp->addAction(actionOpenIssueOnGitHub);
        menuHelp->addAction(actionVisitGitHubWebsite);
        menuHelp->addSeparator();
        menuHelp->addAction(actionAboutRoar);
        toolBarCommands->addAction(actionNew);
        toolBarCommands->addAction(actionOpen);
        toolBarCommands->addAction(actionSave);
        toolBarCommands->addAction(actionSaveAs);
        toolBarCommands->addSeparator();
        toolBarCommands->addAction(actionUndo);
        toolBarCommands->addAction(actionRedo);
        toolBarCommands->addAction(actionCut);
        toolBarCommands->addAction(actionCopy);
        toolBarCommands->addAction(actionPaste);
        toolBarCommands->addAction(actionDelete);
        toolBarCommands->addSeparator();
        toolBarCommands->addAction(actionHideAssetsWindow);
        toolBarCommands->addAction(actionShowAssetsWindow);
        toolBarTools->addAction(actionCursor);
        toolBarTools->addAction(actionRectangle);
        toolBarTools->addAction(actionCircle);
        toolBarTools->addAction(actionFill);
        toolBarTools->addAction(actionLine);
        toolBarTools->addAction(actionText);
        toolBarTools->addAction(actionObject);
        toolBarTools->addAction(actionErase);
        toolBarTools->addAction(actionPickColour);
        toolBarColours->addAction(actionColour00);
        toolBarColours->addAction(actionColour01);
        toolBarColours->addAction(actionColour02);
        toolBarColours->addAction(actionColour03);
        toolBarColours->addAction(actionColour04);
        toolBarColours->addAction(actionColour05);
        toolBarColours->addAction(actionColour06);
        toolBarColours->addAction(actionColour07);
        toolBarColours->addAction(actionColour08);
        toolBarColours->addAction(actionColour09);
        toolBarColours->addAction(actionColour10);
        toolBarColours->addAction(actionColour11);
        toolBarColours->addAction(actionColour12);
        toolBarColours->addAction(actionColour13);
        toolBarColours->addAction(actionColour14);
        toolBarColours->addAction(actionColour15);
        toolBarColours->addAction(actionColourTransparent);
        toolBarColours->addAction(actionFlipColours);
        toolBarColours->addSeparator();
        toolBarColours->addAction(actionIncreaseCanvasWidth);
        toolBarColours->addAction(actionDecreaseCanvasWidth);
        toolBarColours->addAction(actionIncreaseCanvasHeight);
        toolBarColours->addAction(actionDecreaseCanvasHeight);
        toolBarColours->addSeparator();
        toolBarColours->addAction(actionIncreaseCanvasSize);
        toolBarColours->addAction(actionDecreaseCanvasSize);
        toolBarColoursBackground->addAction(actionColourBg00);
        toolBarColoursBackground->addAction(actionColourBg01);
        toolBarColoursBackground->addAction(actionColourBg02);
        toolBarColoursBackground->addAction(actionColourBg03);
        toolBarColoursBackground->addAction(actionColourBg04);
        toolBarColoursBackground->addAction(actionColourBg05);
        toolBarColoursBackground->addAction(actionColourBg06);
        toolBarColoursBackground->addAction(actionColourBg07);
        toolBarColoursBackground->addAction(actionColourBg08);
        toolBarColoursBackground->addAction(actionColourBg09);
        toolBarColoursBackground->addAction(actionColourBg10);
        toolBarColoursBackground->addAction(actionColourBg11);
        toolBarColoursBackground->addAction(actionColourBg12);
        toolBarColoursBackground->addAction(actionColourBg13);
        toolBarColoursBackground->addAction(actionColourBg14);
        toolBarColoursBackground->addAction(actionColourBg15);
        toolBarColoursBackground->addAction(actionColourBgTransparent);
        toolBarColoursBackground->addAction(actionFlipColours);
        toolBarColoursBackground->addSeparator();
        toolBarColoursBackground->addAction(actionIncreaseBrushHeight);
        toolBarColoursBackground->addAction(actionDecreaseBrushHeight);
        toolBarColoursBackground->addAction(actionIncreaseBrushWidth);
        toolBarColoursBackground->addAction(actionDecreaseBrushWidth);
        toolBarColoursBackground->addSeparator();
        toolBarColoursBackground->addAction(actionIncreaseBrushSize);
        toolBarColoursBackground->addAction(actionDecreaseBrushSize);

        retranslateUi(canvas);

        QMetaObject::connectSlotsByName(canvas);
    } // setupUi

    void retranslateUi(QMainWindow *canvas)
    {
        canvas->setWindowTitle(QApplication::translate("canvas", "roar", nullptr));
        actionNew->setText(QApplication::translate("canvas", "&New", nullptr));
#ifndef QT_NO_SHORTCUT
        actionNew->setShortcut(QApplication::translate("canvas", "Ctrl+N", nullptr));
#endif // QT_NO_SHORTCUT
        actionOpen->setText(QApplication::translate("canvas", "&Open", nullptr));
#ifndef QT_NO_SHORTCUT
        actionOpen->setShortcut(QApplication::translate("canvas", "Ctrl+O", nullptr));
#endif // QT_NO_SHORTCUT
        actionSave->setText(QApplication::translate("canvas", "&Save", nullptr));
#ifndef QT_NO_SHORTCUT
        actionSave->setShortcut(QApplication::translate("canvas", "Ctrl+S", nullptr));
#endif // QT_NO_SHORTCUT
        actionSaveAs->setText(QApplication::translate("canvas", "Save &As...", nullptr));
        actionExit->setText(QApplication::translate("canvas", "E&xit", nullptr));
#ifndef QT_NO_SHORTCUT
        actionExit->setShortcut(QApplication::translate("canvas", "Ctrl+X", nullptr));
#endif // QT_NO_SHORTCUT
        actionUndo->setText(QApplication::translate("canvas", "&Undo", nullptr));
#ifndef QT_NO_SHORTCUT
        actionUndo->setShortcut(QApplication::translate("canvas", "Ctrl+Z", nullptr));
#endif // QT_NO_SHORTCUT
        actionRedo->setText(QApplication::translate("canvas", "&Redo", nullptr));
#ifndef QT_NO_SHORTCUT
        actionRedo->setShortcut(QApplication::translate("canvas", "Ctrl+Y", nullptr));
#endif // QT_NO_SHORTCUT
        actionCut->setText(QApplication::translate("canvas", "Cu&t", nullptr));
        actionCopy->setText(QApplication::translate("canvas", "&Copy", nullptr));
        actionPaste->setText(QApplication::translate("canvas", "&Paste", nullptr));
        actionDelete->setText(QApplication::translate("canvas", "De&lete", nullptr));
        actionSolidBrush->setText(QApplication::translate("canvas", "Solid brush", nullptr));
        actionHideAssetsWindow->setText(QApplication::translate("canvas", "Hide assets window", nullptr));
        actionShowAssetsWindow->setText(QApplication::translate("canvas", "Show assets window", nullptr));
        actionCursor->setText(QApplication::translate("canvas", "C&ursor", nullptr));
#ifndef QT_NO_SHORTCUT
        actionCursor->setShortcut(QApplication::translate("canvas", "F2", nullptr));
#endif // QT_NO_SHORTCUT
        actionRectangle->setText(QApplication::translate("canvas", "&Rectangle", nullptr));
#ifndef QT_NO_SHORTCUT
        actionRectangle->setShortcut(QApplication::translate("canvas", "F3", nullptr));
#endif // QT_NO_SHORTCUT
        actionCircle->setText(QApplication::translate("canvas", "&Circle", nullptr));
#ifndef QT_NO_SHORTCUT
        actionCircle->setShortcut(QApplication::translate("canvas", "F4", nullptr));
#endif // QT_NO_SHORTCUT
        actionFill->setText(QApplication::translate("canvas", "&Fill", nullptr));
#ifndef QT_NO_SHORTCUT
        actionFill->setShortcut(QApplication::translate("canvas", "F5", nullptr));
#endif // QT_NO_SHORTCUT
        actionLine->setText(QApplication::translate("canvas", "&Line", nullptr));
#ifndef QT_NO_SHORTCUT
        actionLine->setShortcut(QApplication::translate("canvas", "F6", nullptr));
#endif // QT_NO_SHORTCUT
        actionText->setText(QApplication::translate("canvas", "&Text", nullptr));
#ifndef QT_NO_SHORTCUT
        actionText->setShortcut(QApplication::translate("canvas", "F7", nullptr));
#endif // QT_NO_SHORTCUT
        actionObject->setText(QApplication::translate("canvas", "&Object", nullptr));
#ifndef QT_NO_SHORTCUT
        actionObject->setShortcut(QApplication::translate("canvas", "F8", nullptr));
#endif // QT_NO_SHORTCUT
        actionErase->setText(QApplication::translate("canvas", "&Erase", nullptr));
#ifndef QT_NO_SHORTCUT
        actionErase->setShortcut(QApplication::translate("canvas", "F9", nullptr));
#endif // QT_NO_SHORTCUT
        actionPickColour->setText(QApplication::translate("canvas", "&Pick colour", nullptr));
#ifndef QT_NO_SHORTCUT
        actionPickColour->setShortcut(QApplication::translate("canvas", "F10", nullptr));
#endif // QT_NO_SHORTCUT
        actionFlip->setText(QApplication::translate("canvas", "&Flip", nullptr));
        actionFlipHorizontally->setText(QApplication::translate("canvas", "Flip &horizontally", nullptr));
        actionInvertColours->setText(QApplication::translate("canvas", "&Invert colours", nullptr));
        actionRotate->setText(QApplication::translate("canvas", "&Rotate", nullptr));
        actionTile->setText(QApplication::translate("canvas", "&Tile", nullptr));
        actionViewMelp->setText(QApplication::translate("canvas", "View &melp?", nullptr));
#ifndef QT_NO_SHORTCUT
        actionViewMelp->setShortcut(QApplication::translate("canvas", "F1", nullptr));
#endif // QT_NO_SHORTCUT
        actionOpenIssueOnGitHub->setText(QApplication::translate("canvas", "Open &issue on GitHub", nullptr));
        actionVisitGitHubWebsite->setText(QApplication::translate("canvas", "Visit &GitHub website", nullptr));
        actionAboutRoar->setText(QApplication::translate("canvas", "&About roar", nullptr));
        actionColour00->setText(QApplication::translate("canvas", "Colour #00", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour00->setToolTip(QApplication::translate("canvas", "Colour #00", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour00->setShortcut(QApplication::translate("canvas", "Ctrl+0", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour01->setText(QApplication::translate("canvas", "Colour #01", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour01->setToolTip(QApplication::translate("canvas", "Colour #01", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour01->setShortcut(QApplication::translate("canvas", "Ctrl+1", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour02->setText(QApplication::translate("canvas", "Colour #02", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour02->setToolTip(QApplication::translate("canvas", "Colour #02", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour02->setShortcut(QApplication::translate("canvas", "Ctrl+2", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour03->setText(QApplication::translate("canvas", "Colour #03", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour03->setToolTip(QApplication::translate("canvas", "Colour #03", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour03->setShortcut(QApplication::translate("canvas", "Ctrl+3", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour04->setText(QApplication::translate("canvas", "Colour #04", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour04->setToolTip(QApplication::translate("canvas", "Colour #04", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour04->setShortcut(QApplication::translate("canvas", "Ctrl+4", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour05->setText(QApplication::translate("canvas", "Colour #05", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour05->setToolTip(QApplication::translate("canvas", "Colour #05", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour05->setShortcut(QApplication::translate("canvas", "Ctrl+5", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour06->setText(QApplication::translate("canvas", "Colour #06", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour06->setToolTip(QApplication::translate("canvas", "Colour #06", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour06->setShortcut(QApplication::translate("canvas", "Ctrl+6", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour07->setText(QApplication::translate("canvas", "Colour #07", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour07->setToolTip(QApplication::translate("canvas", "Colour #07", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour07->setShortcut(QApplication::translate("canvas", "Ctrl+7", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour08->setText(QApplication::translate("canvas", "Colour #08", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour08->setToolTip(QApplication::translate("canvas", "Colour #08", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour08->setShortcut(QApplication::translate("canvas", "Ctrl+8", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour09->setText(QApplication::translate("canvas", "Colour #09", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour09->setToolTip(QApplication::translate("canvas", "Colour #09", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour09->setShortcut(QApplication::translate("canvas", "Ctrl+9", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour10->setText(QApplication::translate("canvas", "Colour #10", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour10->setToolTip(QApplication::translate("canvas", "Colour #10", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour10->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+0", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour11->setText(QApplication::translate("canvas", "Colour #11", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour11->setToolTip(QApplication::translate("canvas", "Colour #11", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour11->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+1", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour12->setText(QApplication::translate("canvas", "Colour #12", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour12->setToolTip(QApplication::translate("canvas", "Colour #12", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour12->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+2", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour13->setText(QApplication::translate("canvas", "Colour #13", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour13->setToolTip(QApplication::translate("canvas", "Colour #13", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour13->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+3", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour14->setText(QApplication::translate("canvas", "Colour #14", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour14->setToolTip(QApplication::translate("canvas", "Colour #14", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour14->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+4", nullptr));
#endif // QT_NO_SHORTCUT
        actionColour15->setText(QApplication::translate("canvas", "Colour #15", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColour15->setToolTip(QApplication::translate("canvas", "Colour #15", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColour15->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+5", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourTransparent->setText(QApplication::translate("canvas", "Transparent colour", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourTransparent->setToolTip(QApplication::translate("canvas", "Transparent colour", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourTransparent->setShortcut(QApplication::translate("canvas", "Ctrl+Shift+6", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg00->setText(QApplication::translate("canvas", "Background colour #00", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg00->setToolTip(QApplication::translate("canvas", "Background colour #00", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg00->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+0", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg01->setText(QApplication::translate("canvas", "Background colour #01", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg01->setToolTip(QApplication::translate("canvas", "Background colour #01", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg01->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+1", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg02->setText(QApplication::translate("canvas", "Background colour #02", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg02->setToolTip(QApplication::translate("canvas", "Background colour #02", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg02->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+2", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg03->setText(QApplication::translate("canvas", "Background colour #03", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg03->setToolTip(QApplication::translate("canvas", "Background colour #03", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg03->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+3", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg04->setText(QApplication::translate("canvas", "Background colour #04", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg04->setToolTip(QApplication::translate("canvas", "Background colour #04", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg04->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+4", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg05->setText(QApplication::translate("canvas", "Background colour #05", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg05->setToolTip(QApplication::translate("canvas", "Background colour #05", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg05->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+5", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg06->setText(QApplication::translate("canvas", "Background colour #06", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg06->setToolTip(QApplication::translate("canvas", "Background colour #06", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg06->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+6", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg07->setText(QApplication::translate("canvas", "Background colour #07", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg07->setToolTip(QApplication::translate("canvas", "Background colour #07", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg07->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+7", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg08->setText(QApplication::translate("canvas", "Background colour #08", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg08->setToolTip(QApplication::translate("canvas", "Background colour #08", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg08->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+8", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg09->setText(QApplication::translate("canvas", "Background colour #09", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg09->setToolTip(QApplication::translate("canvas", "Background colour #09", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg09->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+9", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg10->setText(QApplication::translate("canvas", "Background colour #10", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg10->setToolTip(QApplication::translate("canvas", "Background colour #10", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg10->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+0", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg11->setText(QApplication::translate("canvas", "Background colour #11", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg11->setToolTip(QApplication::translate("canvas", "Background colour #11", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg11->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+1", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg12->setText(QApplication::translate("canvas", "Background colour #12", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg12->setToolTip(QApplication::translate("canvas", "Background colour #12", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg12->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+2", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg13->setText(QApplication::translate("canvas", "Background colour #13", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg13->setToolTip(QApplication::translate("canvas", "Background colour #13", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg13->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+3", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg14->setText(QApplication::translate("canvas", "Background colour #14", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg14->setToolTip(QApplication::translate("canvas", "Background colour #14", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg14->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+4", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBg15->setText(QApplication::translate("canvas", "Background colour #15", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBg15->setToolTip(QApplication::translate("canvas", "Background colour #15", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBg15->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+5", nullptr));
#endif // QT_NO_SHORTCUT
        actionColourBgTransparent->setText(QApplication::translate("canvas", "Transparent background colour", nullptr));
#ifndef QT_NO_TOOLTIP
        actionColourBgTransparent->setToolTip(QApplication::translate("canvas", "Transparent background colour", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionColourBgTransparent->setShortcut(QApplication::translate("canvas", "Ctrl+Alt+Shift+6", nullptr));
#endif // QT_NO_SHORTCUT
        actionIncreaseBrushWidth->setText(QApplication::translate("canvas", "Increase brush width", nullptr));
        actionDecreaseBrushWidth->setText(QApplication::translate("canvas", "Decrease brush width", nullptr));
        actionIncreaseBrushHeight->setText(QApplication::translate("canvas", "Increase brush height", nullptr));
        actionDecreaseBrushHeight->setText(QApplication::translate("canvas", "Decrease brush height", nullptr));
        actionIncreaseBrushSize->setText(QApplication::translate("canvas", "Increase brush size", nullptr));
#ifndef QT_NO_SHORTCUT
        actionIncreaseBrushSize->setShortcut(QApplication::translate("canvas", "Ctrl++", nullptr));
#endif // QT_NO_SHORTCUT
        actionDecreaseBrushSize->setText(QApplication::translate("canvas", "Decrease brush size", nullptr));
#ifndef QT_NO_SHORTCUT
        actionDecreaseBrushSize->setShortcut(QApplication::translate("canvas", "Ctrl+-", nullptr));
#endif // QT_NO_SHORTCUT
        actionIncreaseCanvasWidth->setText(QApplication::translate("canvas", "Increase canvas width", nullptr));
#ifndef QT_NO_SHORTCUT
        actionIncreaseCanvasWidth->setShortcut(QApplication::translate("canvas", "Ctrl+Right", nullptr));
#endif // QT_NO_SHORTCUT
        actionDecreaseCanvasWidth->setText(QApplication::translate("canvas", "Decrease canvas width", nullptr));
#ifndef QT_NO_SHORTCUT
        actionDecreaseCanvasWidth->setShortcut(QApplication::translate("canvas", "Ctrl+Left", nullptr));
#endif // QT_NO_SHORTCUT
        actionIncreaseCanvasHeight->setText(QApplication::translate("canvas", "Increase canvas height", nullptr));
#ifndef QT_NO_SHORTCUT
        actionIncreaseCanvasHeight->setShortcut(QApplication::translate("canvas", "Ctrl+Down", nullptr));
#endif // QT_NO_SHORTCUT
        actionDecreaseCanvasHeight->setText(QApplication::translate("canvas", "Decrease canvas height", nullptr));
#ifndef QT_NO_SHORTCUT
        actionDecreaseCanvasHeight->setShortcut(QApplication::translate("canvas", "Ctrl+Up", nullptr));
#endif // QT_NO_SHORTCUT
        actionIncreaseCanvasSize->setText(QApplication::translate("canvas", "Increase canvas size", nullptr));
        actionDecreaseCanvasSize->setText(QApplication::translate("canvas", "Decrease canvas size", nullptr));
        actionDecreaseCellSize->setText(QApplication::translate("canvas", "Decrease cell size", nullptr));
#ifndef QT_NO_TOOLTIP
        actionDecreaseCellSize->setToolTip(QApplication::translate("canvas", "Decrease cell size", nullptr));
#endif // QT_NO_TOOLTIP
        actionIncreaseCellSize->setText(QApplication::translate("canvas", "Increase cell size", nullptr));
#ifndef QT_NO_TOOLTIP
        actionIncreaseCellSize->setToolTip(QApplication::translate("canvas", "Increase cell size", nullptr));
#endif // QT_NO_TOOLTIP
        actionExportAsANSI->setText(QApplication::translate("canvas", "Export as &ANSI...", nullptr));
        actionExportToClipboard->setText(QApplication::translate("canvas", "Export to &clipboard", nullptr));
        actionExportToImgur->setText(QApplication::translate("canvas", "Export to I&mgur...", nullptr));
        actionExportToPastebin->setText(QApplication::translate("canvas", "Export to Pasteb&in...", nullptr));
        actionExportAsPNG->setText(QApplication::translate("canvas", "Export as PN&G...", nullptr));
        actionImportANSI->setText(QApplication::translate("canvas", "Import &ANSI...", nullptr));
        actionImportFromClipboard->setText(QApplication::translate("canvas", "Import from &clipboard", nullptr));
        actionImportSAUCE->setText(QApplication::translate("canvas", "Import &SAUCE...", nullptr));
        actionFlipColours->setText(QApplication::translate("canvas", "Flip colours", nullptr));
#ifndef QT_NO_TOOLTIP
        actionFlipColours->setToolTip(QApplication::translate("canvas", "Flip colours", nullptr));
#endif // QT_NO_TOOLTIP
#ifndef QT_NO_SHORTCUT
        actionFlipColours->setShortcut(QApplication::translate("canvas", "Ctrl+I", nullptr));
#endif // QT_NO_SHORTCUT
        action_Clear_list->setText(QApplication::translate("canvas", "&Clear list", nullptr));
        actionRestore_from_file->setText(QApplication::translate("canvas", "Restore from &file", nullptr));
        menuFile->setTitle(QApplication::translate("canvas", "&File", nullptr));
        menu_Export->setTitle(QApplication::translate("canvas", "&Export...", nullptr));
        menu_Import->setTitle(QApplication::translate("canvas", "&Import...", nullptr));
        menuOpen_Recent->setTitle(QApplication::translate("canvas", "Open &Recent", nullptr));
        menuRes_tore_Snapshot->setTitle(QApplication::translate("canvas", "Res&tore Snapshot", nullptr));
        menuEdit->setTitle(QApplication::translate("canvas", "&Edit", nullptr));
        menuBrush_size->setTitle(QApplication::translate("canvas", "Brush size", nullptr));
        menuCanvas_size->setTitle(QApplication::translate("canvas", "Canvas size", nullptr));
        menuTools->setTitle(QApplication::translate("canvas", "&Tools", nullptr));
        menuOperators->setTitle(QApplication::translate("canvas", "&Operators", nullptr));
        menuHelp->setTitle(QApplication::translate("canvas", "&Help", nullptr));
        toolBarCommands->setWindowTitle(QApplication::translate("canvas", "Commands", nullptr));
        toolBarTools->setWindowTitle(QApplication::translate("canvas", "Tools", nullptr));
        toolBarColours->setWindowTitle(QApplication::translate("canvas", "Colours", nullptr));
        toolBarColoursBackground->setWindowTitle(QApplication::translate("canvas", "Background colours", nullptr));
    } // retranslateUi

};

namespace Ui {
    class canvas: public Ui_canvas {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ROAR_H
