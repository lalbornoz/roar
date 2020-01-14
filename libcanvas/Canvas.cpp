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

#include <algorithm>

#include "../librtl/rtldef.hpp"
#include "Canvas.hpp"

/*
 * Public class functions
 */

Canvas::Canvas(
	SIZE	size
)
: cells(size.h, CELL_LIST(size.w)), cellsUndo{UNDO_CELLS_EMPTY}, size(size)
{
}

bool
Canvas::commit(
	const CELL_LIST&	cells,
	bool			inhibitUndo
)
{
	Canvas::CELL *		cellCanvas;
	Canvas::CELL_LIST	cellsRedo, cellsUndo;
	bool			rc = false;

	for (auto& cell : cells) {
		if ((cell.p.x < this->size.w) && (cell.p.y < this->size.h)) {
			rc = rc ? rc : true;
			cellCanvas = &this->cells[cell.p.y][cell.p.x];
			if (!inhibitUndo)
				cellsRedo.push_back(cell); cellsUndo.push_back(*cellCanvas);
			*cellCanvas = cell;
		}
	}
	if (!inhibitUndo && cellsRedo.size() && cellsUndo.size()) {
		if (this->cellsUndo.index > 0) {
			std::rotate(this->cellsUndo.redoList.begin(), this->cellsUndo.redoList.begin() + this->cellsUndo.index, this->cellsUndo.redoList.end());
			this->cellsUndo.redoList.resize((this->cellsUndo.redoList.size() - this->cellsUndo.index) + 1);
			std::rotate(this->cellsUndo.undoList.begin(), this->cellsUndo.undoList.begin() + this->cellsUndo.index, this->cellsUndo.undoList.end());
			this->cellsUndo.undoList.resize((this->cellsUndo.undoList.size() - this->cellsUndo.index) + 1);
			this->cellsUndo.size -= this->cellsUndo.index, this->cellsUndo.index = 0;
		}
		this->cellsUndo.redoList.insert(this->cellsUndo.redoList.begin(), cellsRedo);
		this->cellsUndo.undoList.insert(this->cellsUndo.undoList.begin(), cellsUndo);
		this->cellsUndo.size++;
	}
	return rc;
}

bool
Canvas::export_(
	Rtl::STATUS&	pstatus,
	std::wstring&	buffer,
	DATA_TYPE	type
)
{
	switch (type) {
	case DTYPE_ANSI: this->exportANSi(pstatus, buffer); break;
	case DTYPE_MIRC: this->exportMiRC(pstatus, buffer); break;
	case DTYPE_SAUCE: this->exportSAUCE(pstatus, buffer); break;
	default: pstatus = Rtl::STATUS_POSIX(EINVAL); break;
	}
	return (bool)(pstatus);
}

bool
Canvas::import(
	Rtl::STATUS&		pstatus,
	Canvas::CELL_MAP&	cells,
	Canvas::SIZE		size
)
{
	this->cells = cells, this->cellsUndo = Canvas::UNDO_CELLS{UNDO_CELLS_EMPTY}, this->size = size;
	return (bool)(pstatus = Rtl::STATUS_NONE_SUCCESS);
}

bool
Canvas::import(
	Rtl::STATUS&		pstatus,
	const std::wstring&	data,
	const DATA_TYPE		type
)
{
	switch (type) {
	case DTYPE_ANSI: this->importANSi(pstatus, data); break;
	case DTYPE_MIRC: this->importMiRC(pstatus, data); break;
	case DTYPE_SAUCE: this->importSAUCE(pstatus, data); break;
	default: pstatus = Rtl::STATUS_POSIX(EINVAL); break;
	}
	if (pstatus)
		this->cellsUndo = Canvas::UNDO_CELLS{UNDO_CELLS_EMPTY};
	return (bool)(pstatus);
}

const Canvas::CELL_LIST *
Canvas::redo(
)
{
	const Canvas::CELL_LIST *	cells = nullptr;

	if (this->cellsUndo.size && (this->cellsUndo.index > 0)) {
		this->cellsUndo.index--, cells = &this->cellsUndo.redoList[this->cellsUndo.index];
		this->commit(*cells, true);
	}
	return cells;
}

const Canvas::CELL_LIST *
Canvas::undo(
)
{
	const Canvas::CELL_LIST *	cells = nullptr;

	if (this->cellsUndo.size && (this->cellsUndo.index < this->cellsUndo.size)) {
		cells = &this->cellsUndo.undoList[this->cellsUndo.index], this->cellsUndo.index++;
		this->commit(*cells, true);
	}
	return cells;
}
