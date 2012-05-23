### -*- coding: utf-8 -*- ####################################################

import os
import datetime
import random
import string
import shutil

from django.core.files.storage import FileSystemStorage
from django.core.files import locks
from django.core.files.move import file_move_safe
from django.conf import settings
from django.utils.encoding import force_unicode, filepath_to_uri

TMP_LIFE_HOURS = getattr(settings, "TMP_LIFE_HOURS", 1)

class RewriteFileSystemStorage(FileSystemStorage):
    """
    Custom filesystem storage. New files always will overwrite old files.
    """
    def _save(self, name, content):
        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        elif not os.path.isdir(directory):
            raise IOError("%s exists and is not a directory." % directory)

        # This file has a file path that we can move.
        if hasattr(content, 'temporary_file_path'):
            file_move_safe(content.temporary_file_path(), full_path)
            content.close()

        # This is a normal uploadedfile that we can stream.
        else:
            # Open file for writting in binary mode
            fd = open(full_path.encode('utf-8'), "wb")
            try:
                locks.lock(fd, locks.LOCK_EX)
                for chunk in content.chunks():
                    fd.write(chunk)
            finally:
                locks.unlock(fd)
                fd.close()

        if settings.FILE_UPLOAD_PERMISSIONS is not None:
            os.chmod(full_path, settings.FILE_UPLOAD_PERMISSIONS)

        return name

    def save(self, name, content):
        """
        Saves new content to the file specified by name. The content should be a
        proper File object, ready to be read from the beginning.
        """
        # Get the proper name for the file, as it will actually be saved.
        if name is None:
            name = content.name

        name = self._save(name, content)

        # Store filenames with forward slashes, even on Windows
        return force_unicode(name.replace('\\', '/'))

    def delete(self, name):
        """
        Rewrote for folders deleting
        """
        name = self.path(name)
        # If the file exists, delete it from the filesystem.
        if os.path.exists(name):
            if os.path.isdir(name):
                shutil.rmtree(name)
            else:
                os.remove(name)

    def create_secure_symlink(self, source_name, result_folder):
        """Create secure symlinks"""
        if not self.exists(source_name):
            raise IOError("%s does not exist." % source_name)

        link_folder = os.path.join(result_folder, self.generate_random_name())
        link_name = os.path.join(link_folder, os.path.split(source_name)[1])

        os.makedirs(self.path(link_folder))

        os.symlink(self.path(source_name), self.path(link_name))

        return link_name

    def generate_random_name(self, length=16, choices=string.ascii_letters):
        """Generate random name"""
        return ''.join(random.choice(choices) for n in range(0, length))

    def delete_old_files(self, directory, remove_dirs=True, tmp_life_hours=TMP_LIFE_HOURS):
        """Remove old files"""
        check_date = datetime.datetime.now() - datetime.timedelta(hours=tmp_life_hours)
        if self.exists(directory):
            file_list = self.listdir(directory)[1]
            if remove_dirs:
                file_list += self.listdir(directory)[0]
            for file_name in file_list:
                if self.created_time(os.path.join(directory, file_name)) < check_date:
                    self.delete(os.path.join(directory, file_name))
