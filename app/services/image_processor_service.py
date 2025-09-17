from typing import Optional
from wand.image import Image as WandImage
import os

class ImageProcessorService:
    @staticmethod
    def process_image(
        input_path: str,
        output_path: str,
        trim: bool = False,
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None,
        quality: int = 0
    ) -> dict:
        """
        Image processing service
        
        Args:
            input_path: Path to input image
            output_path: Path to save processed image
            trim: Whether to trim whitespace
            resize_width: Target width (auto height if only width provided)
            resize_height: Target height (auto width if only height provided)
            quality: quality level (1-100)
        
        Returns:
            dict with image metadata
        """
        with WandImage(filename=input_path) as img:
            # Apply trim if requested
            # Equivalent to -fuzz 5% -trim +repage
            if trim:
                fuzz_value = 0.05 * img.quantum_range
                img.trim(fuzz=fuzz_value)
                img.page = (0, 0, 0, 0)
            
            # Apply resize if requested
            if resize_width and resize_height:
                # Both provided: resize to exact dimensions
                img.resize(resize_width, resize_height)
            elif resize_width:
                # Only width: keep aspect ratio
                img.transform(resize=f'{resize_width}x')
            elif resize_height:
                # Only height: keep aspect ratio
                img.transform(resize=f'x{resize_height}')
            
            # Set compression based on format (skip if compression_level is 0)
            if quality > 0:
                if img.format.lower() in ['jpeg', 'jpg', 'webp']:
                    # JPEG/WebP: Quality compression (1-100)
                    img.compression_quality = quality
                elif img.format.lower() == 'png':
                    png_compression = max(1, min(9, 10 - int(quality / 11)))
                    img.options['png:compression-level'] = str(png_compression)
            
            # Save processed image
            img.save(filename=output_path)
            
            # Return metadata
            return {
                'file_format': img.format.lower(),
                'width': img.width,
                'height': img.height,
                'compression_level': img.compression,
                'file_size_bytes': os.path.getsize(output_path)
            }