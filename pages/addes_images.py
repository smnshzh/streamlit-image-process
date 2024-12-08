import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_classes_ids_with_images(url, base_domain):
    """
    Extract unique classes, IDs, and example images with absolute URLs from the given URL.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(f"Failed to access {url} (Status Code: {response.status_code})")
            return {}, {}

        soup = BeautifulSoup(response.text, 'html.parser')
        class_images = {}
        id_images = {}

        # Extract classes and example images
        for element in soup.find_all(class_=True):
            img_tag = element.find("img")
            if img_tag and img_tag.get("src"):
                img_url = urljoin(base_domain, img_tag["src"])
                for cls in element.get("class", []):
                    if cls not in class_images:
                        class_images[cls] = img_url

        # Extract IDs and example images
        for element in soup.find_all(id=True):
            img_tag = element.find("img")
            if img_tag and img_tag.get("src"):
                if img_tag.get("src").startswith("https"):
                     img_url = img_tag["src"]
                else    
                    img_url = urljoin(base_domain, img_tag["src"])
                element_id = element.get("id")
                if element_id not in id_images:
                    id_images[element_id] = img_url

        return class_images, id_images
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return {}, {}


def scrape_images(url, selector_type, selector, base_domain, start_page=1, end_page=None):
    """
    Scrape images from paginated pages based on the user-selected class or ID.
    Supports dynamic iteration through pages using a for loop.
    """
    all_images = []

    # Iterate over the page range
    end_page = end_page or start_page  # Default to a single page if no range provided
    for page in range(start_page, end_page + 1):
        # Construct the paginated URL
        if "page" in url:
            paginated_url = url+ str(page)
        else:
            paginated_url = url
            
        try:
            response = requests.get(paginated_url)
            if response.status_code != 200:
                st.error(f"Failed to access {paginated_url} (Status Code: {response.status_code})")
                break

            soup = BeautifulSoup(response.text, 'html.parser')

            # Determine the elements based on the selector type
            if selector_type == "class":
                elements = soup.find_all(class_=selector)
            elif selector_type == "id":
                elements = soup.find_all(id=selector)
            else:
                st.error("Invalid selector type.")
                return []

            # Extract images from the elements
            page_images = []
            for element in elements:
                img_tag = element.find("img")
                if img_tag and img_tag.get("src"):
                    img_url = urljoin(base_domain, img_tag["src"])
                    page_images.append({
                        "name": element.text.strip() or "No Name",
                        "image_url": img_url
                    })

            if not page_images:  # Stop if no images are found on the current page
                st.write(f"No images found on page {page}. Ending pagination.")
                break

            all_images.extend(page_images)
            st.write(f"Scraped {len(page_images)} images from page {page}.")
        except Exception as e:
            st.error(f"Error occurred on page {page}: {e}")
            break

    return all_images


# Streamlit App
st.title("Enhanced Web Image Scraper with Pagination")
st.write("Scrape images dynamically from a paginated website.")

# Input URL and base domain
base_url = st.text_input("Enter the base URL (use {page} as a placeholder for pagination):")
base_domain = st.text_input("Enter the main domain (e.g., https://example.com):")
start_page = st.number_input("Start Page:", min_value=1, value=1)
end_page = st.number_input("End Page (optional):", min_value=1, value=1)

if base_url and base_domain:
    current_url = base_url.replace("{page}", str(start_page))
    class_images, id_images = extract_classes_ids_with_images(current_url, base_domain)

    if class_images or id_images:
        st.subheader(f"Available Classes and IDs on Page {start_page}")

        # Display Classes with Examples
        if class_images:
            st.subheader("Available Classes with Examples")
            for cls, img_url in class_images.items():
                st.write(f"Class: {cls}")
                st.image(img_url, width=200)

        # Display IDs with Examples
        if id_images:
            st.subheader("Available IDs with Examples")
            for element_id, img_url in id_images.items():
                st.write(f"ID: {element_id}")
                st.image(img_url, width=200)

        # User Selector Input
        selector_type = st.radio("Choose selector type", ["class", "id"])
        selector = st.text_input(f"Enter the {selector_type} to use for image scraping:")

        if selector:
            images = scrape_images(base_url, selector_type, selector, base_domain, start_page, end_page)
            if images:
                st.subheader("Scraped Images")
                # Display images in a 6-column layout
                cols = st.columns(6)  # Create 6 columns
                for idx, img in enumerate(images):
                    with cols[idx % 6]:  # Distribute images across columns
                        st.image(img['image_url'], caption=img['name'], use_container_width=True)
                        st.write(img['image_url'])

            else:
                st.write("No images found with the given selector.")
    else:
        st.write("No classes or IDs found on this page.")
