/********************************************************************************
** Form generated from reading UI file 'roar_about.ui'
**
** Created by: Qt User Interface Compiler version 5.12.5
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ROAR_ABOUT_H
#define UI_ROAR_ABOUT_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QDialog>
#include <QtWidgets/QDialogButtonBox>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>

QT_BEGIN_NAMESPACE

class Ui_Dialog
{
public:
    QDialogButtonBox *buttonBox;
    QPushButton *pushButton;
    QLabel *label;
    QGraphicsView *graphicsView;

    void setupUi(QDialog *Dialog)
    {
        if (Dialog->objectName().isEmpty())
            Dialog->setObjectName(QString::fromUtf8("Dialog"));
        Dialog->setWindowModality(Qt::ApplicationModal);
        Dialog->resize(546, 141);
        Dialog->setContextMenuPolicy(Qt::DefaultContextMenu);
        Dialog->setStyleSheet(QString::fromUtf8("color: rgb(0, 187, 0);\n"
"background-color: rgb(0, 0, 0);"));
        Dialog->setModal(true);
        buttonBox = new QDialogButtonBox(Dialog);
        buttonBox->setObjectName(QString::fromUtf8("buttonBox"));
        buttonBox->setGeometry(QRect(10, 600, 461, 32));
        buttonBox->setOrientation(Qt::Horizontal);
        buttonBox->setStandardButtons(QDialogButtonBox::Cancel|QDialogButtonBox::Ok);
        pushButton = new QPushButton(Dialog);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));
        pushButton->setGeometry(QRect(250, 100, 160, 32));
        pushButton->setStyleSheet(QString::fromUtf8("color: rgb(0, 0, 0);\n"
"background-color: rgb(233, 233, 233);"));
        label = new QLabel(Dialog);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(140, 10, 401, 71));
        label->setAlignment(Qt::AlignHCenter|Qt::AlignTop);
        graphicsView = new QGraphicsView(Dialog);
        graphicsView->setObjectName(QString::fromUtf8("graphicsView"));
        graphicsView->setGeometry(QRect(10, 10, 121, 121));

        retranslateUi(Dialog);
        QObject::connect(buttonBox, SIGNAL(accepted()), Dialog, SLOT(accept()));
        QObject::connect(buttonBox, SIGNAL(rejected()), Dialog, SLOT(reject()));

        QMetaObject::connectSlotsByName(Dialog);
    } // setupUi

    void retranslateUi(QDialog *Dialog)
    {
        Dialog->setWindowTitle(QApplication::translate("Dialog", "About roar", nullptr));
        pushButton->setText(QApplication::translate("Dialog", "roar!", nullptr));
        label->setText(QApplication::translate("Dialog", "roar -- mIRC art editor for Windows & Linux\n"
"__ROAR_RELEASE_VERSION__\n"
"https://www.github.com/lalbornoz/roar/\n"
"Copyright (c) 2018, 2019 Lucio Andr\303\251s Illanes Albornoz <lucio@lucioillanes.de>\n"
"https://www.lucioillanes.de", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Dialog: public Ui_Dialog {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ROAR_ABOUT_H
