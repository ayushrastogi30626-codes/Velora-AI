from backend.image_generator import generate_image

prompt = "A futuristic cyberpunk city at night with neon lights, ultra realistic, 8k"

image_path = generate_image(prompt)

print("Image saved at:", image_path)