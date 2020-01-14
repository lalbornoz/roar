/*
 * roar -- mIRC art editor for Windows & Linux
 * Copyright (C) 2018, 2019  Lucio Andrés Illanes Albornoz <lucio@lucioillanes.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#include <errno.h>
#include <stdio.h>

#include <string>

#if defined(DEBUG) && defined(_WIN32)
#include <windows.h>
#endif /* defined(DEBUG) && defined(_WIN32) */

#include <QtWidgets/QAction>
#include <QtWidgets/QtWidgets>

#include "../librtl/rtldef.hpp"
#include "CanvasEditorWindow.hpp"

/*
 * Private subroutine prototypes
 */

static void messageOutput(QtMsgType type, const QMessageLogContext &context, const QString &msg);

/*
 * Private subroutines
 */

static void
messageOutput(
	QtMsgType			type,
	const QMessageLogContext &	context,
	const QString &			msg
)
{
	QByteArray	localMsg = msg.toLocal8Bit();

	switch (type) {
	case QtCriticalMsg:
		fprintf(stderr, "Critical: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function); break;
	case QtDebugMsg:
		fprintf(stderr, "Debug: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function); break;
	case QtFatalMsg:
		fprintf(stderr, "Fatal: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function); abort();
	case QtInfoMsg:
		fprintf(stderr, "Info: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function); break;
	case QtWarningMsg:
		fprintf(stderr, "Warning: %s (%s:%u, %s)\n", localMsg.constData(), context.file, context.line, context.function); break;
	}
}

/*
 * Entry point
 */

int
main(
	int	argc,
	char **	argv
)
{
#if defined(DEBUG) && defined(_WIN32)
	if (AllocConsole()) {
		AttachConsole(GetCurrentProcessId());
		(void)freopen("CON", "w", stderr);
		(void)freopen("CON", "r", stdin);
		(void)freopen("CON", "w", stdout);
	} else
		abort();
#endif /* defined(DEBUG) && defined(_WIN32) */
	QApplication		app(argc, argv);
	CanvasEditorWindow	canvasEditorWindow;

	srand(time(NULL));
	qInstallMessageHandler(messageOutput);
	canvasEditorWindow.show();
	return app.exec();
}
