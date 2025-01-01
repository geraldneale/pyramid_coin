import requests
import datetime

def fetch_nft_owner_address(nft_id: str) -> str:
    """
    Fetch the owner address of a given NFT by its ID.
    Returns the owner address or an empty string if not found.
    """
    url = f"https://api.mintgarden.io/nfts/{nft_id}"
    try:
        response = requests.get(url)

        # Check if the response is valid (HTTP 200)
        if response.status_code == 200:
            data = response.json()

            # Check if 'owner_address' and 'id' exist in the response JSON
            owner_address = data.get('owner_address')
            if owner_address and 'id' in owner_address:
                return f"0x{owner_address['id']}"
            else:
                print(f"Owner address ID not found for NFT ID: {nft_id}")
        else:
            print(f"Error fetching data for NFT ID {nft_id}: Status Code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for NFT ID {nft_id}: {e}")
    
    return ""  # Return an empty string if no owner address was found

def save_nft_owner_addresses(nft_ids: list, filename: str) -> int:
    """
    Fetches and writes the owner addresses of NFTs to a specified file.
    Returns the total number of addresses saved.
    """
    counter = 0  # Initialize counter to track the number of successful addresses
    with open(filename, 'w') as file:
        for nft_id in nft_ids:
            owner_address = fetch_nft_owner_address(nft_id)
            if owner_address:  # Only write if we successfully fetched an address
                file.write(f"{owner_address}\n")
                counter += 1  # Increment counter for each successful fetch
    
    return counter  # Return the total number of addresses saved

def generate_filename() -> str:
    """
    Generates a unique filename based on the current date and time.
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"addresses_{timestamp}.txt"

def main() -> None:
    """
    Main function that runs the process of fetching NFT owner addresses and saving them to a file.
    """
    nft_ids = [
    "nft10x8tt7wpfw5atgnhwnfxzx8wsxxc4xl3dmnyhu75pdwhcr9jv97qkxpxth",
    "nft1dswwc5kxww7qvugtpwn5rkmh93kzd28zud729k5lp72dzqz9h7aq69gddh",
    "nft1g32w40etupjnsy5564w3wrmsqqtjqln48pl5mgrn9lf93an7k94sxdqnds",
    "nft1muam2e9z03z4kxrjphu24lhfrzzj4v4zcnf08jkx99phtv39dswqz8j82m",
    "nft1j8a2lsvag2yw6r4vhfz6ujl9vlnpl005rmehzajfle37x0y294ps4w9t46",
    "nft1hh9yzdxgxuwe0c3wnxfhs3ave0hamks64kpaepws75xylsvuugrs5enjs2",
    "nft1rqcqky3z4dgvmr2yaeccr3ztz2q6ehune9yqxwkw0wq0hc5pt8nqkv77u4",
    "nft1ukj4utl98sdm7cercwfq8j9uypq7677x0k94n36rrdccvq0epxtq85ey02",
    "nft18dag0er7hf84njux3r02j3l20wey36r6dtnpd2kgcypctku9yrlspaqfus",
    "nft1060kp3qrsdrf5agenuptk8jwnrfxexc9ywkztc5u34405xkg4elqvpe5s3",
    "nft1pxg0anzrhvfunxv7s2srtjlzyt8zxs5znq9yw5l20wrcjag8q82qv6t4tc",
    "nft16aluxhau8z3sn4xws40tam2vcl2a80gkhdgn7n4gzakxgjacxf0ql0ercv",
    "nft1nfzjqc075xm3hfh066h0ru345czutmwhyprs9ncnzz8xra7wtwrqu526d9",
    "nft1s2cwps6ss3m6p6k2tpylxxrel4sjvt9yxfyjp52m54sf95hrah2sq8aetv",
    "nft1amf8pd58p8cvjrfvvvl54ntdelzlddfkswe35d2sxxcxw4ve5uwqxr3w3a",
    "nft1jdec2v750vzw6jztfpxamltef5nzhnlukd97pt6nze6h6cwmyy2qfqxctx",
    "nft1ktsq9gdlzy6sgagersjk72xg60k8agydy3p9za0rcjam699w9jfsv3xhd2",
    "nft18wp74n3n0vcwz5d9wkrd0crt0y4wg4k3m9vq8p8km5evr6hhxwss3g4579",
    "nft1g6jh6edscmgmvtg65ytfjy9yc5v89tut8ey2jj9l0z5j8a6xtkwqt9q9qs",
    "nft167v9zgf7vk4j3eq8dzmg66320sy5h6pdz0twjkkvtmxwyp69qpfq2cltmk",
    "nft1qlv4uslrp70hut9w40qzry3ep3w08gmcsv3y57zlcmuv6vt6d0rqzwlglu",
    "nft1n0z6d6mjp9p268lhme59t0dfhlvxnexuw9m76avn7ywf9ng8hn5snss9nz",
    "nft1lpgfxnatldh0ehnl2kysmfsztv4knluhuq9gy9s30fpln8y08p3slwyhnz",
    "nft12hvvyeg0ywkydk5ymlmguzkvafk6see30cj2pe7pr2phq2wzyh0sqm8frc",
    "nft1m429vu7atfp3225nyq3w43wg9d6lam0pzccwaaye0v7hte59dpysef476n",
    "nft1m5v9eac73gqd2q6lxs0v3hc0ys3lzvw0wxa0q35v973wg0zwz0hq4lkexm",
    "nft1nwn33n7fzyhwl0vgrerw5nnnf9jkg8sgadffkpt6zzpwk6jzd3psxyjvel",
    "nft15p0wq4p77d6x8swjk8087pfeenu4rrzvmdlqzl33qn7555ytmdps0za88q",
    "nft16kusnpdg7t83g7qkc3fmpu3g4estdw3432lfptr880lsy5u9q7nscxp2qs",
    "nft1lrq52jtssw6yp7wp8j0k53mcegu2a3un2a6prajszwmne0zafwuq40ks4r",
    "nft1yau9x3wm5pzmwrezc4xlpvl4twefu6rwqjcn30q28qhd7pq49zvskqsvqs",
    "nft13tx7n32f28xm8egdf4scutfdp0rjytxhx2qzyfpx9k4qtqsn0gss224k3z",
    "nft1kzdw8egju6jjekd93elmwklmurcyy0fwakh42d25t9hqq87gu0yq0hs29u",
    "nft1gervhmg4vl73mr4r6ugndh35jfn223z65cpj64zl570a68wn6kkqzp3qc7",
    "nft1qschezxgsz4er9y5naqe8z92zlwyspztmszgtetuptaqfrxs73qs0me8ak",
    "nft1j9sasar6646aazxwxyme2pr2yc3qgjrdc7rs40emfxaaptcp6rpsw70t3s",
    "nft1mv4sd0a59uqzk7ev3ftwfsjlucwvj0yp3pyqq774la60weeqnc4qfmrhla",
    "nft1yyagjejld776t4ctp8x3460a2f6fhzkt27ysp5dgq48cv078kv8s2n7x7m",
    "nft1xtntkm56h6uvrqmqf8aq24ufga28qrrg39g4e5u02ha02td4k2uq7hah4x",
    "nft1pq5p9gyt9l5dv7f65tjqzcfq4z375wtrgvnyugcgeg65c3mvp53sfnffhd",
    "nft1ds9dkmfxkslaafkcy7ncjkswxe2m5nv3d3xcn8x0afnnt5dzg74q2xffr9",
    "nft1vzepw26nqaapj7j2yskueh8h7ka5j9ex7l3j3kk8k4r0kymgte2qu30nka",
    "nft1thq5fuuaa89tp9rhdt97nerjrvq4e2edzknu8qnkmz6h3rn0d04qg9azg9",
    "nft10te2hv40fcwyneefxtxmuldqz2wd63ylu9met3v9jc2cnctzq5ps64nq9z",
    "nft1vehylptn0yedj2gsm6m75cjxxru0n9kakueyj7mj0kvmhfl6mq7sl08djj",
    "nft17qku60y7dsmr55j6q4fnlj49kx8fqg0emh9s442fc7f06f6flq5qm4jtw3",
    "nft1sm7gtzyz42njdmca4w9xmsj7v97p0d080uqq83wkvngepyqaae9q06ptte",
    "nft10tt40jnsrv6jlqzwdvvgs2qqu4uj7tmma3lq878hwjvr6gl938nqclzsk8",
    "nft156hkdktaafmetepvwsyh48sh4dsh20pwl0suvwuc7xp7al33ykcs78r7e6",
    "nft1tgec7hkkn640qc3gdxhhlmtcs3l2yl58upmflr4z8rzfkpxjn4xsmhep0z",
    "nft10tlylr53pjj6ly20n38gs3ky867qr5thfskccu96trdfr3aadeys8q23jy",
    "nft1cfx66r43c7cskwyj0gclmxf0dwz9nga5ymp7gsl65r4q4mg0wr7sa49td6",
    "nft1dg7a38w669a74slp5dlrzykf9dumrnxjepc3plhlg0hee75kd7zsueajq3",
    "nft15yc2wtndk9yxhmq9t74n7jzv8j6xk35g0ry3ujj8yufq3q6qulcs8pwuvs",
    "nft1hftv8xg9a837h7ndrvdamveus5l2py69vtp32nrjqm0vkt8s0vsqqjv8rc",
    "nft1ptpfhk3cp55r7d7ed7zqsj9wx5d8xl7mev48wefr744jrn3cjeasn9wgtq",
    "nft1neukm9j7v4krq0hjx6zs0ugf0de6a7s3c56a9pq44t9ej4czhqkqxn7qsu",
    "nft1lqkhchg3qgt5jft9apevp3mm930gx0kx68mj7kfs4q8wtfh9yp9q4ndq75",
    "nft1nlhklht62dpx9s326sshvl53r46vtq4u0wl5zt0s30uatapalw0sykzu5h",
    "nft170nd8nx0wx6zws6nvk3ahll5q04e2fjm548le266qvm933m0wdvsng0dgt",
    "nft1qp4vx3vct4hdesc9l2jzys0jzxnrc6tdw92ptm7wjwckj223h2us43q6kv",
    "nft1x7mxryntlck8mqpslzzzkdu5mjkkmanumdq5gekyr3j68csxfz9sccgg7n",
    "nft19ph0zh9vy5p88wxf95shg79shmnua0dj06an58tgd4qw089wtxps80qnr9",
    "nft1k85mtxwydxe59vmqmxnqlal94xvvwr4gjsrwy9g2t56nlwdnktvs7j6zf2",
    "nft1zzaw2y7ms6c6rfk6awkt6hjr337cuc009mm5nhmdeefr3xvvaftqz9a8m3",
    "nft10r3ggde5889tz46zxvhv52shwkfrutmyrkhndngf2cwrlepkq6zs7gr4tv",
    "nft1lldrrzul5w26yxpylhrf0tl0p9hslxnh3d4dwnvj0sw4wgjled7suamqys",
    "nft1t56kn5kcqnj64nd5chwa6ha7u0zjgdgm0y3nrcaylzr9em73hzlsfxjnkn",
    "nft1l7t24zv4x0kzld3m5cvv8jwexg7n36h85udcjsean80kvxfpnq3qvs3snc",
    "nft1d8u8se8jyxev9kaxdn8fet4k5ea4nv6n97uxz4c0qn748fee9dfs8tsykd",
    "nft1glqafca8027wckft7adc50zgufglv26e6pkq40azgd8ua405hjtssdautd",
    "nft1cpvnzw0dvgd96ys7pc5vng4c3nuur76fs4ttuf6pj2ttpuut4n0q4nvuvs",
    "nft1ha53g9g3k3pyf6yxa9ccaslhh6z9y3f7f0g8628snsux0pzqg7tsa7fl95",
    "nft1x2vrv2t9apw3zkv4f0r7dax22mqnclmtyh6nlne0cy3c47t7fe7qtqgwx7",
    "nft1uya2ysxuqa8qsjwy0vgkhmvdepqavnejc7wkydsrqdj8wxekruzsfks67y",
    "nft1u03hnztr95tzvddv25qv2c2tmc3crjqcmsmkla7vw5vye36m7ryqcrxaze",
    "nft1vg0r74j79eqycq0al22jmnq776mw0usptcsu9yt2rg59tcjvpyeseda97q",
    "nft1z02x2l8hr3jf2vfj8aqcjglz9tquql5xh7pgv6j0dz0h4kn3jlzs7n2cxf",
    "nft1hccfy44sptvle242vlrpp4hkzl8qgqf70wetpa4kjmtz6nvdy87q48ujyt",
    "nft1auj4mez2qkdrz6qj9ssdk770w2qejgnj5c8tmze8pfanxrdl4t3qhj2pxd"
    ]
    
    # Generate a unique filename based on the current date and time
    filename = generate_filename()

    # Fetch and save NFT owner addresses, then get the total count
    saved_addresses_count = save_nft_owner_addresses(nft_ids, filename)

    print(f"JSON IDs have been written to {filename}")
    print(f"Total addresses saved: {saved_addresses_count}")
if __name__ == "__main__":
    main()
