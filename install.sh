#!/usr/bin/env bash

# CONFIG SECTION ---------------------------------------------------------------

#
# string PIP
#
# path to pip application, can be overriden using external variable passed to
# script
#

# PIP is not set

#
# bool INSTALL_LOCALLY
#
# determines whether application ought to be installed locally (in a pip
# compliant fashion)
#

# INSTALL_LOCALLY is not set

# INITIALIZATION SECTION -------------------------------------------------------

# Determine project directory, compensate for calling from outside CWD via
# a symlink with readlink
PROJECT_DIRECTORY="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
[[ -z ${PROJECT_DIRECTORY} ]] && \
PROJECT_DIRECTORY="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Determine whether we should install locally in pip-compliant fashion
for arg in "$@"
do
	[[ "$arg" == "--user" ]] && INSTALL_LOCALLY=1
done

# Determine which pip to use, prefer pip3 to pip
[[ -z $PIP ]] && PIP=$(command -v pip3)
[[ -z $PIP ]] && PIP=$(command -v pip)

# INSTALL SECTION --------------------------------------------------------------

# Determine which pip to use, prefer pip3 to pip
[[ -z $PIP ]] && PIP=$(command -v pip3)
[[ -z $PIP ]] && PIP=$(command -v pip)

# Provided user is root and chose not to install application locally
# install globally, otherwise install locally. Should local installation
# fail, attempt global installation using sudo (if present in system).
[[ $UID -eq 0 ]] && [[ -z $INSTALL_LOCALLY || $INSTALL_LOCALLY != "0" ]] && {
	echo " :: Attempting to install globally from \`$PROJECT_DIRECTORY'."
	$PIP install "$PROJECT_DIRECTORY"
} || {
	echo " :: Attempting to install locally from \`$PROJECT_DIRECTORY'."
	$PIP install --user "$PROJECT_DIRECTORY" || {
		[[ ! -z $(command -v sudo) ]] && {
			echo " !! Local installation failed." >&2
			echo " :: Attempting to install globally using sudo."
			sudo $PIP install "$PROJECT_DIRECTORY"
		}
	}
}
