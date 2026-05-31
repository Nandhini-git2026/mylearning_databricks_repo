# 1.
name = "Nandhini B"
print(name.lower())
print(name.upper())
print(name.capitalize())

# 2.
number = "9999999990"
masked = number[:2]+"******"+number[-2:]
print(masked)

# 3.
song = "shape OF you"
artist = "nandhini B"

print(f"{song.title()} - {artist.title()}") #Every first letter of string will be capitalized
print(f"{song.capitalize()} - {artist.capitalize()}") #only starting the string will be capitalized

# 4.

location = "Chennai Central"
fixed_location = location.replace("Chennai Central","Tambaram")
print(fixed_location)

# 5. To pick booking id in a msg

message = "Your uber booking id is: UB12345.Please keep it safe"
booking_id= message.split(":")[1].split(".")[0].strip()
print(booking_id)

# 6. To check promocode in a msg

promo_msg="use zomato100 to get 100 off in your first order"
if "zomato100" in promo_msg:
    print("Offer applied")

# 7. Returns position of the word

feedback = "the driver was polite and the ride was smooth"
print(feedback.index("polite"))
print(feedback.find("polite"))


# 8. To pick first letter from first name and last name

name = "nandhini balakrishnan"
initials = [word[0].upper() for word in name.split()] # will print as list
print(initials)
initials ="".join([word[0].upper() for word in name.split()]) # to not print as list
print(initials)

# my logic from above using append
full_name= ""
for word in name.split(" "):
   full_name +=word[0].upper()
print("My logic:",full_name)

#9. Trim the unwanted space before/after string

dirty_input = "   airport   "
print(dirty_input.strip())

# 10. to print length of string

word1 = "the trip was amazing and the car was clean"
word_count = len(word1.split())
print(word_count)

