---
tags: [blog]
is_published: false

name: "Micro-benchmarking in Rust."
description: "How do i verify which methodology is better to solve a problem"
date: 2024-01-26
cover: "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*FjbFVoofbgaKNE9SxqtZ0Q.jpeg"
coverAlt: "Micro-benchmarking in Rust"
logo:
  image: "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*FjbFVoofbgaKNE9SxqtZ0Q.jpeg"
  fallback:
    text: "R"
    bgColor: "bg-indigo-500"

caseStudy:
  challenge: "How do i verify which methodology is better to solve a problem"
  solution: "We use micro-benchmarks; in Rust."
  results:
    - "Sometimes, the imrpovements are marginal."
  links:
    - text: "Read Original"
      url: "https://medium.com/@birnadin?source=post_page-----2682235a5a08--------------------------------"
    - text: "Home"
      url: "https://www.methebe.com"
---

# Micro-benchmarking in Rust 101

> migrated from old system. If something doesn't make sense, it probably due to the way migration script works. Please refer tot he original versio

[Medium:](https://medium.com/@birnadin?source=post_page-----2682235a5a08--------------------------------)

Not a professional at benchmarking, but a wannabe!

We craft software everyday some marvelous some shameful. If we stumble upon 2 approaches for a single goal, how do we logically and statistically determine which one to choose?

**Benchmarks!** Let’s learn it. Skip next section to jump right it. Note the subtitle and this is for fun. The conclusion is already out of the bag decades ago.

The Story
---------

I recently implemented bubble sort in rust. Intrigued by rust’s Iterators, I asked ChatGPT to spit out something resembling the TheAlgorithms implementation but use suitable amount of iterators. This is what it came up ⤵️

```
pub fn bubble\_sort\_iter<T: Ord + Clone>(arr: &mut \[T\]) {
    let mut n = arr.len();
    let mut v = Vec::new(); // because windows need immmutable parent
    arr.clone\_into(&mut v);

    while n > 0 {
        let mut last\_swapped = 0;

        // Using iterator to find the last swap position
        for (i, window) in v.windows(2).enumerate().take(n - 1) {
            if window\[0\] > window\[1\] {
                arr.swap(i, i + 1);
                last\_swapped = i + 1;
            }
        }

        n = last\_swapped;
    }
}
```

The procedural implementation I came up with after the GitHub scavenge is…

```
pub fn bubble\_sort<T: Ord>(arr: &mut \[T\]) {
    if arr.is\_empty() {
        return;
    }
    let mut sorted = false;
    let mut n = arr.len();
    while !sorted {
        sorted = true;
        for i in 0..n - 1 {
            if arr\[i\] > arr\[i + 1\] {
                arr.swap(i, i + 1);
                sorted = false;
            }
        }
        n -= 1;
    }
}


```

Not a ton of difference. Just the for loop turned into `window` function. Which one is better?

The rest
--------

We could sprinkle some GNU Core Utils magic to measure the performance, but I am lazy and not a statistician. Luckily someone created a crate to _micro-benchmark_ rust functions — [criterion](https://crates.io/crates/criterion) — which is conveniently pulled using…

```
cargo add criterion
```

Now we define our experiments.

1.  Generate random data to sort
2.  Test each function
3.  Measure the latency

You can find the data generation script at the end of this story. <TK: add python script>. I created 5 files each grow my 10 fold or so. Our functions require `i32`. So let’s first create a utility function to read a file and prepare the data.

```
fn read\_data\_from\_file<P>(filename: P) -> io::Result<Vec<i32>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    let buffer = io::BufReader::new(file);
    Ok(buffer
        .lines()
        .map(|line| line.unwrap().parse::<i32>().unwrap())
        .collect::<Vec<i32>>())
}
```

I hope you know File IO at this point; if not follow be and sign up for my [newsletter](https://enigmabits.substack.com/) when I publish my part 5 of series on Learning Rust with 99 problems.

[

99 problems to understand Rust — Part 1
---------------------------------------

### what could you learn by building a CLI tool to find GCD of integers?

blog.stackademic.com

](https://blog.stackademic.com/99-problems-to-understand-rust-part-1-53c6899b460e?source=post_page-----2682235a5a08--------------------------------)

Now, onto the juicy part. We’ve got two implementations of bubble sort — the traditional one and the fancy iterator-based one. Let’s pit them against each other.

```
// since we are doing this for few different batches
let mut group = c.benchmark\_group(format!("Bubble Sort - {} items", size));

// procedural
group.bench\_function("bubble\_sort", |b| {
    b.iter(|| {
        let mut data\_clone = data.clone();
        bubble\_sort(black\_box(&mut data\_clone));
    })
});

// relatively more declarative
group.bench\_function("bubble\_sort\_iter", |b| {
    b.iter(|| {
        let mut data\_clone = data.clone();
        bubble\_sort\_iter(black\_box(&mut data\_clone));
    })
});

group.finish();
```

Some enigmatic constructs to expose, but ain’t much. What’s happening here? First off, notice the `format!` macro. It’s not just there for show; it gives us an easy way to label our benchmarks depending on the size of the data we’re sorting. Handy, eh?

Next, `group.bench_function` - this is where the magic happens. We’re taking each of our functions (`bubble_sort` and `bubble_sort_iter`) for a spin. The `b.iter()` call, ah, that’s Criterion.rs doing its thing, making sure we're measuring performance in a **statistically** significant way.

It’s not just running our code once; oh no, that would be too easy. It’s running it multiple times, measuring each run.

> It’s like timing a sprinter on different tracks to get the average speed.

Then, there’s `black_box`. This nifty function tells the compiler to ignore. It’s like a magician’s black box, keeping our data safe from the compiler magic.

And finally, `group.finish()`. We're done setting up the battle; let's see who wins. Criterion conveniently creates a `bench` command on cargo. Let’s bench!

Graphs!
-------

Last screenshot is full of statistics. Since we are learning, let’s plot some graph shall we. First of all the obvious metric — Mean runtime i.e. latency.

Hope you can read graphs

Honestly, I did not expect the iterators to win. Because we have a cloning and then windowing overhead. Yet, DAMN! difference is not that bad. Remember the scale; it is in nanoseconds. We are not slow, just relatively lagging.

**Note** the last group. Iterators outshines. I don’t know what happened. Theoretically cloning 100K numbers should have taken longer. My bet is on my computer. This was run on a development machine. Though, I’d give it a pass since this is learning and not for any serious business decisions. But you should keep an eye for these kinds of stuff.

time range table

This is more confusing. Did I screw up entering values into Excel? Someone explain the result to me.

Epilogue
========

Otherwise, as promised that’s how you benchmark in rus. At least as of my study of StackOverflow and Blogs on rust.

MY take from this is to use groups and expand the sample data. May be something wrong with the randomly seed data could mess up the results.

Always look out for outliers. Here I have almost 3.0% here and then. Read the output for particular results.

**References.** Below are things I used to compile this benchmark. As indicated previously, the bubble sort algorithm is inspired by TheAlgorithms source code.

Random data generator.

```
#!/usr/bin/env python3

import argparse
import random

def generate\_random\_data(filename, num\_items, range\_start, range\_end):
    with open(filename, 'w') as f:
        for \_ in range(num\_items):
            f.write(f"{random.randint(range\_start, range\_end)}\\n")

if \_\_name\_\_ == "\_\_main\_\_":
    parser = argparse.ArgumentParser(description="Generate a file with random integers.")
    parser.add\_argument("filename", type=str, help="The name of the output file")
    parser.add\_argument("num\_items", type=int, help="Number of random integers to generate")
    parser.add\_argument("range\_start", type=int, help="Start of the range for random integers")
    parser.add\_argument("range\_end", type=int, help="End of the range for random integers")

    args = parser.parse\_args()

    generate\_random\_data(args.filename, args.num\_items, args.range\_start, args.range\_end)
    print(f"Generated {args.num\_items} random integers in {args.filename}")
```

If you have enjoyed this reading a clap and a follow would be useful. And read my series of my learning journey in Rust to ease off my college degree subjects.

[

99 problems to understand Rust — Part 1
---------------------------------------

### what could you learn by building a CLI tool to find GCD of integers?

blog.stackademic.com

](https://blog.stackademic.com/99-problems-to-understand-rust-part-1-53c6899b460e?source=post_page-----2682235a5a08--------------------------------)

See you on the next one. 🤗

Till then it’s _metheBE_ signing off 👋.
