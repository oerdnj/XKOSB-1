# QR Code Steganography

The program here is a simplified version of [1].  It (ab)uses the
correction mechanism of the QR codes to insert scrambled but not
encrypted version of the secret text into the QR code image.

First the plaintext message is converted into the QR code.  The QR
code is then loaded into the memory and the secret message is first
scrambled using Baker's Map into a rectangle smaller than the QR code
to honour the empty margins of the QR code and then XORed with the
image data.  The resulting PNG is then saved.  The image looks like
slightly corrupted QR code.

Secret message recovery is done by decoding the QR code - the decoding
mechanism ignores the glitches - the plaintext is encoded again using
the same mechanism as when we were encoding it.  The images are XORed
again and reverse Baker's map is applied on the differences.  This
gives us the unscrambled secret text.

## Encoding

`python3 ./scramble.py <output.png> "plaintext" "secret text"`

## Decoding

`python3 ./unscramble.py <input.png>`

## Possible improvements and known bugs

1. Validate the Baker's Map implementation.  However, the main problem
   is a lack of implementations in just any language.  There's one
   implementation in Rust and couple of pages in Matlab, but it's also
   absolutely unclear if those are correct.

   This implementation in Python is modeled after [2].

2. Instead of using Baker's map, find the edges in the image and
   encode the secret text by expanding the edges of the image, so it
   looks more innoculous to a human eye.

3. Explore the possibility of XOR-ing the hidden text as a QR code
   as aligned image in the centre of the visible text QR code.  The
   error correction of the envelope might survive this and the result
   would look more innocent to a human eye.

# References

1. M. Alajmi, I. Elashry, H. S. El-Sayed and O. S. Farag Allah,
   "Steganography of Encrypted Messages Inside Valid QR Codes," in IEEE
   Access, vol. 8, pp. 27861-27873, 2020, doi: 10.1109/ACCESS.2020.2971984.

2. https://codegolf.stackexchange.com/questions/48027/discrete-bakers-map
