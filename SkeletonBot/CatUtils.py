import aiohttp
import json

async def getCatPicture():
    result = ""
    async with aiohttp.get('https://aws.random.cat/meow') as r:
        if r.status == 200:
            js = await r.json()
            result += js['file']
        else:
           result += "Could not get the file: " + str(js['file'])
        print(result)
        return result

def main():
    print(getCatPicture())

if __name__ == '__main__':
    main()        