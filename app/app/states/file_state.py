import reflex as rx
import os


class FileState(rx.State):
    uploaded_files: list[str] = []
    is_uploading: bool = False

    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        if not files:
            return
        yield FileState.set_is_uploading(True)
        try:
            for file in files:
                upload_data = await file.read()
                outfile = (
                    rx.get_upload_dir() / file.filename
                )
                with open(outfile, "wb") as f:
                    f.write(upload_data)
                if file.filename not in self.uploaded_files:
                    self.uploaded_files.append(
                        file.filename
                    )
            yield rx.toast.success(
                f"Successfully uploaded {len(files)} file(s)."
            )
        except Exception as e:
            yield rx.toast.error(f"Upload failed: {e}")
        finally:
            yield FileState.set_is_uploading(False)

    @rx.event
    def delete_file(self, filename: str):
        try:
            filepath = rx.get_upload_dir() / filename
            if os.path.exists(filepath):
                os.remove(filepath)
            self.uploaded_files = [
                f
                for f in self.uploaded_files
                if f != filename
            ]
            return rx.toast.info(f"Deleted {filename}.")
        except Exception as e:
            return rx.toast.error(
                f"Failed to delete {filename}: {e}"
            )