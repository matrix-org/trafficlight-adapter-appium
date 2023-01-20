
def main():
    adapter = Adapter()


if __name__ == '__main__':
  adapter = Appium()
  adapter.setup()
  adapter.login('matrix.org','wibble','wobble')
  time.sleep(5)
  adapter.finish()
 
